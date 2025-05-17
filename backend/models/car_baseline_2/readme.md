# 🔍 Fuzzy-XGBoost 模型部署（精简预测版）

本项目使用模糊特征增强和 XGBoost 模型，已封装训练过程，开源版本仅提供：
- 模型预测脚本 `main_fuzzy_predict.py`
- 模型权重 `fuzzy_xgboost_model.pkl`
- 模糊特征 `X_test_combined.pkl`

无需重新训练或生成特征，运行以下命令即可获得模型预测效果：

```bash
python main_fuzzy_predict.py

