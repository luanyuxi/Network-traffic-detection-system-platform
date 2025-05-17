import os
import time
import json
import joblib
import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, f1_score
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from pre import preprocess_data  # 你已有的预处理脚本

# 路径设置
model_filename = "fuzzy_xgboost_model.pkl"
test_feature_file = "X_test_combined_XG.pkl"

# 重新预处理标签（必须和训练一致）
X_train, X_test, y_train, y_test = preprocess_data()
label_encoder = LabelEncoder()
y_test = label_encoder.fit_transform(y_test)

# 加载 fuzzy 特征
if not os.path.exists(test_feature_file):
    raise FileNotFoundError("❌ 缺少 X_test_combined_XG.pkl，请先运行 fuzzy 特征生成流程。")

X_test_combined = joblib.load(test_feature_file)

# 平衡测试集
def balance_test_set(X, y):
    n = min(sum(y == 0), sum(y == 1), 3500)
    i0 = resample(np.where(y == 0)[0], n_samples=n, replace=False, random_state=42)
    i1 = resample(np.where(y == 1)[0], n_samples=n, replace=False, random_state=42)
    idx = np.concatenate([i0, i1])
    return X[idx], y[idx]

# 模型评估函数
def assess_model(y_true, y_pred):
    report = classification_report(y_true, y_pred, output_dict=True)
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='macro')
    return acc, f1, report

# 推理函数
def run_xgboost_predict():
    try:
        model = joblib.load(model_filename)
        print("✅ 模型加载成功")

        X_bal, y_bal = balance_test_set(X_test_combined, y_test)
        dtest = xgb.DMatrix(X_bal)

        start = time.time()
        preds = model.predict(dtest)
        end = time.time()

        acc, f1, report = assess_model(y_bal, preds)

        return {
            "with_rules": {
                "Accuracy": acc,
                "Precision": float(report["macro avg"]["precision"]),
                "Recall": float(report["macro avg"]["recall"]),
                "F1-score": float(report["macro avg"]["f1-score"]),
            }
        }
    except Exception as e:
        return {"error": str(e)}

# 执行
if __name__ == "__main__":
    result = run_xgboost_predict()
    print(json.dumps(result, indent=4))
