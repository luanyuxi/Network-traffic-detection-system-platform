import os
import time
import numpy as np
import pandas as pd
import xgboost as xgb
import json
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
import joblib  # 用于保存和加载模型
import gc  # 垃圾回收

# 模型文件路径
model_filename = os.path.join(os.path.dirname(__file__),'xgboost_model.pkl')

# 使用 preprocess_data 从 PCAP 文件中解析并返回训练和测试数据
from pre import preprocess_data
X_train, X_test, y_train, y_test = preprocess_data()

# 调整噪声幅度
np.random.seed(None)
train_noise = np.random.normal(0, 0.2, X_train.shape)  # 降低噪声的标准差
X_train += train_noise

test_noise = np.random.normal(0, 0.2, X_test.shape)  # 同样为测试集添加较小的噪声
X_test += test_noise




# 标签编码
label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(y_train)
y_test = label_encoder.transform(y_test)

# 确认数据维度
assert X_train.shape[0] == y_train.shape[0], "训练数据和标签数量不匹配"
assert X_test.shape[0] == y_test.shape[0], "测试数据和标签数量不匹配"

# 将数据转换为 XGBoost 所需的 DMatrix 格式
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# 设置 XGBoost 参数
params = {
    'objective': 'multi:softmax',  # 多分类
    'num_class': len(np.unique(y_train)),  # 类别数量
    'tree_method': 'hist',  # 使用直方图加速训练
    'predictor': 'cpu_predictor',  # 使用 CPU 预测
    'max_depth': 4,  # 最大树深度
    'eta': 0.2,  # 学习率
    'eval_metric': 'mlogloss',  # 评估指标
    'lambda': 1,  # L2 正则化
    'alpha': 0,  # L1 正则化
}

# 平衡测试集的标签 0 和 1
def balance_test_set(X_test, y_test):
    label_0_count = sum(y_test == 0)
    label_1_count = sum(y_test == 1)
    min_count = min(label_0_count, label_1_count)

    # 获取标签为 0 和 1 的数据索引
    label_0_count = sum(y_test == 0)
    label_1_count = sum(y_test == 1)

    min_count = min(label_0_count, label_1_count, 2000)  # 确保总数不超过 15000
    index_0 = np.where(y_test == 0)[0]
    index_1 = np.where(y_test == 1)[0]
    index_0_downsampled = resample(index_0, replace=False, n_samples=min_count, random_state=42)
    index_1_downsampled = resample(index_1, replace=False, n_samples=min_count, random_state=42)

    balanced_indices = np.concatenate([index_0_downsampled, index_1_downsampled])

    # 如果 X_test 是 DataFrame，使用 iloc 进行行索引，否则直接使用 NumPy 风格索引
    if isinstance(X_test, pd.DataFrame):
        X_test_balanced = X_test.iloc[balanced_indices]
    else:
        X_test_balanced = X_test[balanced_indices]

    y_test_balanced = y_test[balanced_indices]

    return X_test_balanced, y_test_balanced

# 模型评估函数
def assess_model(true_labels, model_pred, model_name):
    cm = confusion_matrix(true_labels, model_pred)
    report = classification_report(true_labels, model_pred, output_dict=True)
    f1 = f1_score(true_labels, model_pred, average='macro')

    # 计算每个类别的 TN, FP, FN, TP
    class_metrics = {}
    for i in range(len(cm)):
        tp = int(cm[i, i])  # 将 int64 转换为标准 Python int
        fp = int(cm[:, i].sum() - tp)
        fn = int(cm[i, :].sum() - tp)
        tn = int(cm.sum() - (tp + fp + fn))
        class_metrics[f"Class {i}"] = {
            "TP": tp,
            "TN": tn,
            "FP": fp,
            "FN": fn
        }

    return accuracy_score(true_labels, model_pred), f1, report, class_metrics

# 训练 XGBoost 模型并保存
def train_and_save_model():
    # 执行交叉验证以找到最佳的 boosting 轮数
    cv_results = xgb.cv(
        params,
        dtrain,
        num_boost_round=100,  # 迭代轮数
        nfold=5,  # 5折交叉验证
        early_stopping_rounds=10,
        metrics='mlogloss',
        as_pandas=True,
        seed=42
    )

    # 找到最佳的 boosting 轮数
    best_num_boost_rounds = cv_results['test-mlogloss-mean'].idxmin()

    # 使用最佳 boosting 轮数训练模型
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

# 主要执行函数
def run_xgboost():
    try:
        import os
        if os.path.exists(model_filename):
            # 加载保存的模型
            model = load_and_test_model()
        else:
            # 训练新模型并保存
            model = train_and_save_model()

        # 评估模型
        X_test_balanced, y_test_balanced = balance_test_set(X_test, y_test)
        dtest_balanced = xgb.DMatrix(X_test_balanced)

        # 开始测试计时
        start_time = time.time()

        # 预测
        test_preds_balanced = model.predict(dtest_balanced)

        # 结束计时
        end_time = time.time()
        elapsed_time = end_time - start_time

        accuracy_balanced, f1_balanced, report_balanced, class_metrics_balanced = assess_model(y_test_balanced, test_preds_balanced, 'XGBoost')

        # 返回评估结果
        return {
            "without_rules": {
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
    result = run_xgboost()
    if result:
        print(json.dumps(result, indent=4))
    else:
        print("No valid results generated.")
