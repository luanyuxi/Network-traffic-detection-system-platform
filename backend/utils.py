import os
import json
import re
import subprocess
import gc
from typing import Optional
from fastapi import APIRouter, HTTPException
import psutil
import joblib

# 数据集根目录路径
BASE_DIR = r"F:/FastAPI/backend/models/"

# 初始化路由
router = APIRouter()

def clean_memory():
    """清理系统内存。"""
    gc.collect()
    psutil.virtual_memory()

def run_script(script_name, working_dir):
    """在指定路径执行 Python 脚本并获取 JSON 格式的标准输出。"""
    try:
        script_path = os.path.join(working_dir, script_name)
        result = subprocess.run(
            ['python', script_path],
            cwd=working_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        match = re.search(r'({.*})', result.stdout, re.DOTALL)
        if match:
            json_output = match.group(0)
            return json.loads(json_output)
        else:
            print("No JSON output found in script output.")
            return None
    except Exception as e:
        print(f"Error running script: {e}")
        return None


def list_datasets(scene):
    """列出特定场景的数据集文件夹。"""
    datasets = [
        f for f in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, f))
           and f.lower().startswith(scene.lower())
    ]
    return datasets

def get_dataset_path(base_dir: str, dataset_name: str, sub_path: Optional[str] = None) -> str:
    """构建数据集的完整路径，包含子目录."""
    dataset_path = os.path.join(base_dir, dataset_name)
    if sub_path:
        dataset_path = os.path.join(dataset_path, sub_path)
    return dataset_path

def load_pkl_file(filepath):
    """加载 .pkl 文件内容。"""
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return joblib.load(f)
    else:
        raise FileNotFoundError(f"File not found: {filepath}")

def load_rules_from_json(dataset_name):
    """从指定数据集加载规则信息。"""
    rules_path = os.path.join(BASE_DIR, dataset_name, "rules", "rules.json")
    if os.path.exists(rules_path):
        with open(rules_path, 'r') as f:
            rules_data = json.load(f)
        return rules_data
    else:
        raise FileNotFoundError(f"Rules file not found for dataset: {dataset_name}")

# 动态加载模型和生成规则的结果
def get_model_results(model: str, scene: str, dataset_name: str):
    project_dir = os.path.join(BASE_DIR, dataset_name)

    # 确保项目文件夹存在
    if not os.path.exists(project_dir):
        return None

    # 运行 t-SNE 结果生成脚本
    tsne_results = run_script('t_SNE.py', project_dir)
    if not tsne_results:
        print("Failed to generate or load t-SNE results from t-SNE.py")
        return None

    if model.lower() == "xgboost":
        xgboost_results = run_script('main_XG.py', project_dir)  # 无规则 XGBoost
        fuzzy_xgboost_results = run_script('main_FU_XG.py', project_dir)  # 有规则 XGBoost
        print("XGBoost results:", xgboost_results)
        print("Fuzzy XGBoost results:", fuzzy_xgboost_results)

        final_results = {
            "scene": scene if scene else "Encryption Traffic Scene",
            "dataset": dataset_name,
            "models": {
                "XGBoost": {
                    "without_rules": xgboost_results.get("without_rules", {}) if xgboost_results else {},
                    "with_rules": fuzzy_xgboost_results.get("with_rules", {}) if fuzzy_xgboost_results else {}
                }
            },
            "tsne_coordinates": tsne_results.get('tsne_coordinates'),
            "selected_clusters": tsne_results.get('selected_clusters')
        }
    elif model.lower() == "randomforest":
        rf_results = run_script('main_RF.py', project_dir)  # 无规则 Random Forest
        fuzzy_rf_results = run_script('main_FU_RF.py', project_dir)  # 有规则 Random Forest
        final_results = {
            "scene": scene if scene else "Encryption Traffic Scene",
            "dataset": dataset_name,
            "models": {
                "Random Forest": {
                    "without_rules": rf_results.get("without_rules", {}) if rf_results else {},
                    "with_rules": fuzzy_rf_results.get("with_rules", {}) if fuzzy_rf_results else {}
                }
            },
            # 加入 t-SNE 结果
            "tsne_coordinates": tsne_results.get('tsne_coordinates'),
            "selected_clusters": tsne_results.get('selected_clusters')
        }
    else:
        return None
    # 在 get_model_results 函数返回前添加调试打印
    print("Returning model results:", json.dumps(final_results, indent=4))


    # 清理内存
    clean_memory()

    # 返回结果字典
    return final_results

@router.get("/api/datasets/{scene}")
async def get_datasets(scene: str):
    datasets = list_datasets(scene)
    if not datasets:
        raise HTTPException(status_code=404, detail="No datasets found for this scene.")
    return {"datasets": datasets}


# 新的 API 端点来获取规则信息
@router.get("/api/rules/{dataset_name}")
async def get_rules_information(dataset_name: str):
    rules_path = os.path.join(BASE_DIR, dataset_name, "rules", "rules.json")
    if not os.path.exists(rules_path):
        raise HTTPException(status_code=404, detail="Rules file not found for dataset: {}".format(dataset_name))

    with open(rules_path, 'r', encoding='utf-8') as file:
        rules_data = json.load(file)

    # 去掉外层的 "rules_information" 嵌套，直接返回内容
    simplified_data = {
        "rules_information": {
            "scene": rules_data.get("scene", ""),
            "dataset": rules_data.get("dataset", ""),
            "number_of_rules": rules_data["rules_information"].get("number_of_rules", 0),
            "number_of_features": rules_data["rules_information"].get("number_of_features", 0),
            "detailed_rules": rules_data["rules_information"].get("detailed_rules", [])
        }
    }

    return simplified_data

# 包含模型结果的 API 端点
@router.get("/api/results/{model}/{scene}/{dataset_name}")
async def get_model_information(model: str, scene: str, dataset_name: str):
    try:
        result_data = get_model_results(model=model, scene=scene, dataset_name=dataset_name)
        if result_data:
            return result_data
        else:
            raise HTTPException(status_code=404, detail="No result data available.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
