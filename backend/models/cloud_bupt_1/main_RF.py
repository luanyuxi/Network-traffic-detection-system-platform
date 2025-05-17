import time
import numpy as np
import pandas as pd
import os
import json  # 添加 json 模块来格式化输出
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
import gc  # 添加垃圾回收模块
import joblib  # 用于保存和加载模型

from pre import preprocess_data

# 加载或生成数据集
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

# 训练好的模型文件路径
model_filename = os.path.join(os.path.dirname(__file__),'random_forest_model.pkl')


def assess_model(true_labels, model_pred, model_name):
    cm = confusion_matrix(true_labels, model_pred)
    report = classification_report(true_labels, model_pred, output_dict=True)
    f1 = f1_score(true_labels, model_pred, average='macro')

    # 计算每个类别的 TN, FP, FN, TP
    class_metrics = {}
    for i in range(len(cm)):
        tp = int(cm[i, i])  # 将 NumPy 类型转换为标准 int 类型
        fp = int(cm[:, i].sum() - tp)  # 确保所有数据为标准 Python 类型
        fn = int(cm[i, :].sum() - tp)
        tn = int(cm.sum() - (tp + fp + fn))
        class_metrics[f"Class {i}"] = {
            "TP": tp,
            "TN": tn,
            "FP": fp,
            "FN": fn
        }

    return accuracy_score(true_labels, model_pred), f1, report, class_metrics


def train_and_save_model():
    # 超参数搜索
    # 1. 调整 n_estimators
    scorel = []
    for i in range(0, 200, 10):
        RFC = RandomForestClassifier(n_estimators=i + 1, n_jobs=-1, random_state=0)
        score = cross_val_score(RFC, X_train, y_train, cv=10).mean()
        scorel.append(score)

    best_n_estimators = (scorel.index(max(scorel)) * 10) + 1

    # 2. 调整 max_features
    param_grid = {'max_features': ['sqrt', 'log2', None]}
    RFC = RandomForestClassifier(n_estimators=best_n_estimators, random_state=0)
    GS = GridSearchCV(RFC, param_grid, cv=10)
    GS.fit(X_train, y_train)
    best_max_features = GS.best_params_['max_features']

    # 3. 调整 criterion
    param_grid = {'criterion': ['gini', 'entropy']}
    RFC = RandomForestClassifier(n_estimators=best_n_estimators, random_state=0, max_features=best_max_features)
    GS = GridSearchCV(RFC, param_grid, cv=10)
    GS.fit(X_train, y_train)
    best_criterion = GS.best_params_['criterion']

    # 4. 调整 max_depth
    param_grid = {'max_depth': np.arange(1, 20, 1)}
    RFC = RandomForestClassifier(n_estimators=best_n_estimators, random_state=0, max_features=best_max_features,
                                 criterion=best_criterion)
    GS = GridSearchCV(RFC, param_grid, cv=10)
    GS.fit(X_train, y_train)
    best_max_depth = GS.best_params_['max_depth']

    # 使用最优参数训练 Random Forest 模型
    RFC = RandomForestClassifier(
        n_estimators=best_n_estimators,
        random_state=0,
        max_features=best_max_features,
        criterion=best_criterion,
        max_depth=best_max_depth
    )
    RFC.fit(X_train, y_train)

    # 保存模型
    joblib.dump(RFC, model_filename)


# 加载并测试模型
def load_and_test_model():
    # 加载模型
    RFC = joblib.load(model_filename)

    # 开始计时
    start_time = time.time()

    label_0_count = sum(y_test == 0)
    label_1_count = sum(y_test == 1)

    min_count = min(label_0_count, label_1_count, 2000)  # 确保总数不超过 15000
    index_0 = np.where(y_test == 0)[0]
    index_1 = np.where(y_test == 1)[0]
    index_0_downsampled = resample(index_0, replace=False, n_samples=min_count, random_state=42)
    index_1_downsampled = resample(index_1, replace=False, n_samples=min_count, random_state=42)

    balanced_indices = np.concatenate([index_0_downsampled, index_1_downsampled])

    # 如果 X_test 是 DataFrame，使用 iloc 进行行索引
    if isinstance(X_test, pd.DataFrame):
        X_test_balanced = X_test.iloc[balanced_indices]
    else:
        X_test_balanced = X_test[balanced_indices]  # NumPy 风格索引

    y_test_balanced = y_test[balanced_indices]

    # 使用平衡后的测试集进行预测
    RFC_test_pred_balanced = RFC.predict(X_test_balanced)

    # 结束计时
    end_time = time.time()
    elapsed_time = end_time - start_time

    # 评估模型
    accuracy_balanced, f1_balanced, report_balanced, class_metrics_balanced = assess_model(y_test_balanced,
                                                                                           RFC_test_pred_balanced,
                                                                                           'Random Forest')

    # 返回平衡测试集的评估结果
    RandomForest_results_balanced = {
        "without_rules": {
            "Accuracy": float(accuracy_balanced),
            "precision": float(report_balanced["macro avg"]["precision"]),
            "recall": float(report_balanced["macro avg"]["recall"]),
            "f1-score": float(report_balanced["macro avg"]["f1-score"]),
            #"Class Metrics": class_metrics_balanced,
            #"Total Execution Time": f"{elapsed_time:.2f} seconds"
        }
    }

    return RandomForest_results_balanced



if __name__ == "__main__":
    try:
        # 如果模型文件存在，则加载并测试，否则训练模型并保存
        import os

        if os.path.exists(model_filename):
            result = load_and_test_model()  # 只进行测试
        else:
            train_and_save_model()  # 训练并保存模型
            result = load_and_test_model()  # 测试

        print(json.dumps(result, indent=4))  # 打印 JSON 格式的结果
    except Exception as e:
        print(f"Error: {str(e)}")

# 清理内存
gc.collect()