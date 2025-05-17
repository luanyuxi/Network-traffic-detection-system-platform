import os

import numpy as np
import pandas as pd
import xgboost as xgb
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, f1_score, confusion_matrix
from sklearn.utils import resample
import json
import time

from pre import preprocess_data

# 模型文件路径
model_filename =  os.path.join(os.path.dirname(__file__), 'fuzzy_xgboost_model.pkl')  # 使用你上传的模型路径
rules_filename = os.path.join(os.path.dirname(__file__),'generated_rules.pkl' ) # 新增规则文件路径

# 加载并测试模型
def load_and_test_model(dtest):
    start_time = time.time()
    model = joblib.load(model_filename)
    print("Model loaded successfully.")
    elapsed_time = time.time() - start_time

    # 预测
    test_preds = model.predict(dtest)
    return test_preds


# 平衡测试集并确保样本总数为 15000
def balance_test_set(X_test, y_test, target_size=15000):
    label_0_count = sum(y_test == 0)
    label_1_count = sum(y_test == 1)

    samples_per_class = target_size // 2
    samples_per_class = min(samples_per_class, label_0_count, label_1_count)

    index_0 = np.where(y_test == 0)[0]
    index_1 = np.where(y_test == 1)[0]

    index_0_downsampled = resample(index_0, replace=False, n_samples=samples_per_class, random_state=None)  # 随机采样
    index_1_downsampled = resample(index_1, replace=False, n_samples=samples_per_class, random_state=None)

    balanced_indices = np.concatenate([index_0_downsampled, index_1_downsampled])

    X_test_balanced = X_test.values[balanced_indices]
    y_test_balanced = y_test[balanced_indices]

    return X_test_balanced, y_test_balanced


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


# 主要执行函数
def run_fuzzy_xgboost():
    try:
        X_train, X_test, y_train, y_test = preprocess_data()

        # 设置随机种子为 None，以确保每次不同的随机数
        np.random.seed()  # 随机种子为当前时间

        # 加入随机噪声
        noise_scale = np.random.uniform(0.000000012, 0.00000002)  # 随机选择噪声幅度
        test_noise = np.random.normal(0, noise_scale, X_test.shape)
        X_test += test_noise

        label_encoder = LabelEncoder()
        y_train = label_encoder.fit_transform(y_train)
        y_test = label_encoder.transform(y_test)

        if model_filename:
            # 平衡测试集
            X_test_balanced, y_test_balanced = balance_test_set(X_test, y_test, target_size=15000)
            dtest_balanced = xgb.DMatrix(X_test_balanced)

            # 测试并评估
            start_time = time.time()
            test_preds_balanced = load_and_test_model(dtest_balanced)
            elapsed_time = time.time() - start_time

            # 评估模型
            accuracy_balanced, f1_balanced, report_balanced, class_metrics_balanced = assess_model(y_test_balanced,
                                                                                                   test_preds_balanced)

            return {
                "with_rules": {
                    "Accuracy": accuracy_balanced,
                    "precision": float(report_balanced["macro avg"]["precision"]) if report_balanced else 0.0,
                    "recall": float(report_balanced["macro avg"]["recall"]) if report_balanced else 0.0,
                    "f1-score": float(report_balanced["macro avg"]["f1-score"]) if report_balanced else 0.0,
                    #"Class Metrics": class_metrics_balanced
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
