import os
import time
import numpy as np
import pandas as pd
import xgboost as xgb
import json
from joblib import Parallel, delayed
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
import joblib  # 用于保存和加载模型
import gc

from pre import preprocess_data
from get_matrix import get_matrix
from FCM import FCM1115, FCM1115_te
from A_es import A_es0
from y_te_out import Y_te_out

# 模型文件路径
model_filename =  os.path.join(os.path.dirname(__file__), 'fuzzy_xgboost_model.pkl')

# 调用 preprocess_data 函数进行数据预处理
X_train, X_test, y_train, y_test = preprocess_data()


# 调整噪声幅度
np.random.seed(None)


test_noise = np.random.normal(0, 0.00000007, X_test.shape)  # 同样为测试集添加较小的噪声
X_test += test_noise

# 对标签进行编码
label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(y_train)
y_test = label_encoder.transform(y_test)

# 确认数据维度
assert X_train.shape[0] == y_train.shape[0], "训练数据和标签数量不匹配"
assert X_test.shape[0] == y_test.shape[0], "测试数据和标签数量不匹配"

# 平衡测试集的标签 0 和 1
def balance_test_set(X_test, y_test):

    # 平衡测试集样本总数为 15000
    label_0_count = sum(y_test == 0)
    label_1_count = sum(y_test == 1)

    min_count = min(label_0_count, label_1_count, 5500)  # 确保总数不超过 15000
    index_0 = np.where(y_test == 0)[0]
    index_1 = np.where(y_test == 1)[0]
    index_0_downsampled = resample(index_0, replace=False, n_samples=min_count, random_state=42)
    index_1_downsampled = resample(index_1, replace=False, n_samples=min_count, random_state=42)

    balanced_indices = np.concatenate([index_0_downsampled, index_1_downsampled])

    # 使用平衡后的数据
    X_test_balanced = X_test[balanced_indices]
    y_test_balanced = y_test[balanced_indices]

    return X_test_balanced, y_test_balanced

# Fuzzy clustering 和 regression 迭代
def fuzzy_iteration(loop, X_train, y_train, X_test, y_test, c, m, chunk_size):
    X_train = X_train.values if isinstance(X_train, pd.DataFrame) else X_train
    X_test = X_test.values if isinstance(X_test, pd.DataFrame) else X_test

    m, te_m, data_train_re, data_test_re = get_matrix(loop, y_train, y_test)
    U, V, c = FCM1115(X_train, c=c, m=m)
    U_te = FCM1115_te(V, c, X_test, m=m)
    A = A_es0(data_train_re, U, X_train, c, chunk_size)

    y_out_train = np.zeros((X_train.shape[0], A.shape[1]))
    for i in range(0, X_train.shape[0], chunk_size):
        end = min(i + chunk_size, X_train.shape[0])
        expanded_X_train = np.zeros((end - i, (X_train.shape[1] + 1) * c))
        for j in range(c):
            expanded_X_train[:, j * (X_train.shape[1] + 1):(j + 1) * (X_train.shape[1] + 1)] = np.hstack(
                [np.ones((end - i, 1)), X_train[i:end]]) * U[i:end, j:j + 1]
        y_out_train[i:end] = expanded_X_train @ A

    y_te_out = Y_te_out(A, X_test, U_te, c, chunk_size)

    return y_out_train, y_te_out

# 并行执行 Fuzzy clustering 和 regression
num_iterations = 10
c = 5
m = 2.5
chunk_size = 10000

results = Parallel(n_jobs=-1)(
    delayed(fuzzy_iteration)(loop, X_train, y_train, X_test, y_test, c, m, chunk_size) for loop in range(num_iterations)
)

# 合并结果
y_out_list = [result[0] for result in results]
y_te_out_list = [result[1] for result in results]

# 使用模糊聚类方法的平均预测值作为特征
fuzzy_train_features = np.mean(y_out_list, axis=0)
fuzzy_test_features = np.mean(y_te_out_list, axis=0)

# 将原始特征与模糊聚类特征结合
X_train_combined = np.column_stack((X_train, fuzzy_train_features))
X_test_combined = np.column_stack((X_test, fuzzy_test_features))

# 将数据转换为 DMatrix 格式，供 XGBoost 使用
dtrain = xgb.DMatrix(X_train_combined, label=y_train)
dtest = xgb.DMatrix(X_test_combined, label=y_test)

# 设置 XGBoost 参数
params = {
    'objective': 'multi:softmax',
    'num_class': len(np.unique(y_train)),
    'tree_method': 'hist',
    'max_depth': 4,
    'eta': 0.2,
    'eval_metric': 'mlogloss',
    'lambda': 1,
    'alpha': 0,
}

# 训练 XGBoost 模型并保存
def train_and_save_model():
    # 进行交叉验证以确定最佳树数
    cv_results = xgb.cv(
        params,
        dtrain,
        num_boost_round=100,
        nfold=5,
        early_stopping_rounds=10,
        metrics='mlogloss',
        as_pandas=True,
        seed=42
    )
    best_num_boost_rounds = cv_results['test-mlogloss-mean'].idxmin()

    # 使用最佳树数训练模型
    model = xgb.train(params, dtrain, num_boost_round=best_num_boost_rounds)

    # 保存模型
    joblib.dump(model, model_filename)
    print("Model saved successfully.")

    return model

# 加载并测试模型
def load_and_test_model():
    # 加载模型
    model = joblib.load(model_filename)
    print("Model loaded successfully.")

    return model

# 模型评估函数
def assess_model(true_labels, model_pred, model_name):
    cm = confusion_matrix(true_labels, model_pred)
    report = classification_report(true_labels, model_pred, output_dict=True)
    f1 = f1_score(true_labels, model_pred, average='macro')

    # 计算每个类别的 TN, FP, FN, TP
    class_metrics = {}
    for i in range(len(cm)):
        tp = int(cm[i, i])  # 确保转换为 int
        fp = int(cm[:, i].sum() - tp)
        fn = int(cm[i, :].sum() - tp)
        tn = int(cm.sum() - (tp + fp + fn))
        class_metrics[f"Class {i}"] = {
            "TP": tp,
            "TN": tn,
            "FP": fp,
            "FN": fn
        }

    return float(accuracy_score(true_labels, model_pred)), float(f1), report, class_metrics

# 主要执行函数
def run_fuzzy_xgboost():
    try:
        import os
        if os.path.exists(model_filename):
            model = load_and_test_model()
        else:
            model = train_and_save_model()

        # 评估模型
        X_test_balanced, y_test_balanced = balance_test_set(X_test_combined, y_test)
        dtest_balanced = xgb.DMatrix(X_test_balanced)

        # 开始测试计时
        start_time = time.time()

        test_preds_balanced = model.predict(dtest_balanced)

        # 结束计时
        end_time = time.time()
        elapsed_time = end_time - start_time

        accuracy_balanced, f1_balanced, report_balanced, class_metrics_balanced = assess_model(y_test_balanced, test_preds_balanced, 'XGBoost')

        # 封装结果
        return {
            "with_rules": {
                "Accuracy": accuracy_balanced,
                "precision": float(report_balanced["macro avg"]["precision"]),
                "recall": float(report_balanced["macro avg"]["recall"]),
                "f1-score": float(report_balanced["macro avg"]["f1-score"]),
                #"Class Metrics": class_metrics_balanced,
                #"Total Execution Time": f"{elapsed_time:.2f} seconds"
            }
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {}

# 如果是直接运行该文件，输出 JSON 格式的结果
if __name__ == "__main__":
    result = run_fuzzy_xgboost()
    if result:
        print(json.dumps(result, indent=4))
    else:
        print("No valid results generated.")
