import os
import numpy as np
import json
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from pre import preprocess_data


# 模型文件路径
model_filename = os.path.join(os.path.dirname(__file__),'random_forest_model_fuzzy.pkl')

# 数据预处理
X_train, X_test, y_train, y_test = preprocess_data()



from sklearn.impute import SimpleImputer

# 在预处理后处理 NaN 值
imputer = SimpleImputer(strategy="median")
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# 调整噪声幅度
np.random.seed(None)
train_noise = np.random.normal(0, 0.0015, X_train.shape)
X_train += train_noise

test_noise = np.random.normal(0, 0.0015, X_test.shape)
X_test += test_noise

# 标签编码
label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(y_train)
y_test = label_encoder.transform(y_test)

# 确认数据维度
assert X_train.shape[0] == y_train.shape[0], "训练数据和标签数量不匹配"
assert X_test.shape[0] == y_test.shape[0], "测试数据和标签数量不匹配"

def load_and_test_model(X_test_combined, y_test):
    X_test_combined = joblib.load("X_test_combined_RF.pkl")
    RFC = joblib.load("random_forest_model_fuzzy.pkl")
    preds = RFC.predict(X_test_combined)
    return preds

# 模型评估函数
def assess_model(true_labels, model_pred):
    try:
        cm = confusion_matrix(true_labels, model_pred)
        report = classification_report(true_labels, model_pred, output_dict=True)
        accuracy = accuracy_score(true_labels, model_pred)
        f1 = f1_score(true_labels, model_pred, average='macro')

        class_metrics = {}
        for i in range(len(cm)):
            tp = int(cm[i, i])
            fp = int(cm[:, i].sum() - tp)
            fn = int(cm[i, :].sum() - tp)
            tn = int(cm.sum() - (tp + fp + fn))
            class_metrics[f"Class {i}"] = {"TP": tp, "TN": tn, "FP": fp, "FN": fn}

        return accuracy, f1, report, class_metrics
    except Exception as e:
        print(f"Error in assess_model: {str(e)}")
        return 0.0, 0.0, {}, {}


def balance_test_set(X_test_combined, y_test):
    # 计算每个类别的样本数量
    label_0_count = sum(y_test == 0)
    label_1_count = sum(y_test == 1)

    # 设定每个类别的最大样本数量
    max_count_per_class = 7500

    # 确定每个类别的下采样索引
    index_0 = np.where(y_test == 0)[0]
    index_1 = np.where(y_test == 1)[0]

    # 如果某个类别的样本数量大于 7500，就进行下采样
    index_0_downsampled = resample(index_0, replace=False, n_samples=min(label_0_count, max_count_per_class),
                                   random_state=42)
    index_1_downsampled = resample(index_1, replace=False, n_samples=min(label_1_count, max_count_per_class),
                                   random_state=42)

    # 合并下采样后的索引
    balanced_indices = np.concatenate([index_0_downsampled, index_1_downsampled])

    # 创建平衡后的测试集
    X_test_balanced = X_test_combined[balanced_indices]
    y_test_balanced = y_test[balanced_indices]

    return X_test_balanced, y_test_balanced


def run_model_from_pkl():
    try:
        # 加载保存的测试特征和模型
        X_test_combined = joblib.load("X_test_combined_RF.pkl")
        RFC = joblib.load("random_forest_model_fuzzy.pkl")

        # 平衡测试集
        X_test_combined_balanced, y_test_balanced = balance_test_set(X_test_combined, y_test)

        # 模型预测
        RFC_test_pred = RFC.predict(X_test_combined_balanced)

        # 模型评估
        accuracy, f1, report, _ = assess_model(y_test_balanced, RFC_test_pred)

        return {
            "with_rules": {
                "Accuracy": accuracy,
                "precision": float(report["macro avg"]["precision"]),
                "recall": float(report["macro avg"]["recall"]),
                "f1-score": float(report["macro avg"]["f1-score"]),
            }
        }

    except Exception as e:
        print(f"[ERROR] {e}")
        return {}



if __name__ == "__main__":
    result = run_model_from_pkl()
    print(json.dumps(result, indent=4))

