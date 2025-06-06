import os
import numpy as np
import json
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV, train_test_split
from sklearn.utils import resample
import joblib  # 用于保存和加载模型

from pre import preprocess_data


# 模型文件路径
model_filename = os.path.join(os.path.dirname(__file__),'random_forest_model_fuzzy.pkl')

# 数据预处理
X_train, X_test, y_train, y_test = preprocess_data()

# 调整噪声幅度
np.random.seed(None)
train_noise = np.random.normal(0, 0.1, X_train.shape)  # 降低噪声的标准差
X_train += train_noise

test_noise = np.random.normal(0, 0.1e-4, X_test.shape)  # 同样为测试集添加较小的噪声
X_test += test_noise

# 标签编码
label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(y_train)
y_test = label_encoder.transform(y_test)

# 确认数据维度
assert X_train.shape[0] == y_train.shape[0], "训练数据和标签数量不匹配"
assert X_test.shape[0] == y_test.shape[0], "测试数据和标签数量不匹配"

# 训练 Random Forest 模型并保存
def train_and_save_model(X_train_combined, y_train):
    # RandomForest hyperparameter tuning
    scorel = []
    for i in range(0, 200, 10):
        RFC = RandomForestClassifier(n_estimators=i + 1, n_jobs=-1, random_state=0)
        score = cross_val_score(RFC, X_train_combined, y_train, cv=10).mean()
        scorel.append(score)

    best_n_estimators = (scorel.index(max(scorel)) * 10) + 1

    # Fine-tune n_estimators around the optimal value
    scorel = []
    for i in range(120, 140):
        RFC = RandomForestClassifier(n_estimators=i, n_jobs=-1, random_state=0)
        score = cross_val_score(RFC, X_train_combined, y_train, cv=10).mean()
        scorel.append(score)

    best_n_estimators = [*range(120, 140)][scorel.index(max(scorel))]

    # Optimize max_features
    param_grid = {'max_features': ['sqrt', 'log2', None]}
    RFC = RandomForestClassifier(n_estimators=best_n_estimators, random_state=0)
    GS = GridSearchCV(RFC, param_grid, cv=10)
    GS.fit(X_train_combined, y_train)
    best_max_features = GS.best_params_['max_features']

    # Optimize criterion
    param_grid = {'criterion': ['gini', 'entropy']}
    RFC = RandomForestClassifier(n_estimators=best_n_estimators, random_state=0, max_features=best_max_features)
    GS = GridSearchCV(RFC, param_grid, cv=10)
    GS.fit(X_train_combined, y_train)
    best_criterion = GS.best_params_['criterion']

    # Optimize max_depth
    param_grid = {'max_depth': np.arange(1, 20, 1)}
    RFC = RandomForestClassifier(n_estimators=best_n_estimators, random_state=0, max_features=best_max_features,
                                 criterion=best_criterion)
    GS = GridSearchCV(RFC, param_grid, cv=10)
    GS.fit(X_train_combined, y_train)
    best_max_depth = GS.best_params_['max_depth']

    # 使用最优参数训练 Random Forest 模型
    RFC = RandomForestClassifier(n_estimators=best_n_estimators, random_state=0,
                                 max_features=best_max_features, criterion=best_criterion, max_depth=best_max_depth)
    RFC.fit(X_train_combined, y_train)

    # 保存模型
    joblib.dump(RFC, model_filename)
    #print("Model saved successfully.")


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
        f1 = f1_score(true_labels, model_pred, average='macro')

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
    except Exception as e:
        print(f"Error in assess_model: {str(e)}")
        return 0.0, 0.0, {}, {}

# 平衡测试集标签 0 和 1
def balance_test_set(X_test_combined, y_test):
    # 平衡测试集样本总数为 15000
    label_0_count = sum(y_test == 0)
    label_1_count = sum(y_test == 1)

    min_count = min(label_0_count, label_1_count, 2500)  # 确保总数不超过 15000
    index_0 = np.where(y_test == 0)[0]
    index_1 = np.where(y_test == 1)[0]
    index_0_downsampled = resample(index_0, replace=False, n_samples=min_count, random_state=42)
    index_1_downsampled = resample(index_1, replace=False, n_samples=min_count, random_state=42)

    balanced_indices = np.concatenate([index_0_downsampled, index_1_downsampled])

    # 使用平衡后的数据
    X_test_combined_balanced = X_test_combined[balanced_indices]
    y_test_balanced = y_test[balanced_indices]

    return X_test_combined_balanced, y_test_balanced


# 主要执行函数
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
