import mimetypes
import os
from datetime import timedelta
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from .auth import create_access_token, authenticate_user, Token

from pydantic import BaseModel, Field
from starlette.responses import JSONResponse, FileResponse

# 使用绝对路径导入模块
from backend.utils import get_model_results, list_datasets, clean_memory, load_rules_from_json
from backend.auth import Token, create_access_token, authenticate_user  # 导入函数

from fastapi import FastAPI
from backend.utils import router as utils_router

app = FastAPI()

# 注册 utils 路由
app.include_router(utils_router)

# 数据集根目录路径
BASE_DIR = r"F:/FastAPI/backend/models/"

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",  # ← 加上这个
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Token管理
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login/access_token")


# 用户注册模型
class UserRegistrationModel(BaseModel):
    registration_code: str = Field(alias="code")
    username: str
    password: str
    confirm_password: str = Field(alias="confirmPassword")


# 用户登录模型
class LoginModel(BaseModel):
    username: str
    password: str


# 请求模型
class ModelRequest(BaseModel):
    model: str
    scene: str
    dataset_name: str


# 用户注册端点
@app.post("/v1/user/register")
async def register_user(user: UserRegistrationModel):
    if user.password != user.confirm_password:
        return {"error": "Passwords do not match."}
    return {"message": "User registered successfully!"}


# 登录端点，返回JWT访问令牌
@app.post("/api/admin/login/access_token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # 使用 authenticate_user 函数验证用户名和密码
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 获取用户信息
@app.get("/api/admin/login/getinfo")
async def get_info(token: str = Depends(oauth2_scheme)):
    return {"message": "User information retrieved successfully"}


# 获取可用场景的接口
@app.get("/api/scenes")
async def get_scenes():
    return ["Car", "Encrypt", "Cloud", "Iot", "Mix"]


# 获取场景下的数据集的接口
@app.get("/api/datasets/{scene}")
async def get_datasets(scene: str):
    datasets = list_datasets(scene)
    if not datasets:
        raise HTTPException(status_code=404, detail="No datasets found for this scene.")
    return {"datasets": datasets}


# 读取指定数据集的文件内容
@app.get("/api/dataset/{dataset_name}")
async def read_dataset(dataset_name: str):
    dataset_path = os.path.join(BASE_DIR, dataset_name, "data")

    if not os.path.exists(dataset_path):
        raise HTTPException(status_code=404, detail="Dataset not found")

    file_contents = {}
    for filename in os.listdir(dataset_path):
        file_path = os.path.join(dataset_path, filename)
        if os.path.isfile(file_path):
            if filename.endswith(".pcap"):
                file_contents[filename] = f"{file_path} (binary file, pcap format)"
            elif filename.endswith(".csv"):
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        file_contents[filename] = f.read()
                except UnicodeDecodeError:
                    file_contents[filename] = "无法读取内容（编码不支持）"
            else:
                mime_type, _ = mimetypes.guess_type(file_path)
                file_contents[filename] = f"{file_path} ({mime_type or 'unknown type'})"

    return JSONResponse(content=file_contents)


# 用于下载特定文件的端点
@app.get("/api/dataset/{dataset_name}/file/{filename}")
async def get_file(dataset_name: str, filename: str):
    file_path = os.path.join(BASE_DIR, dataset_name, "data", filename)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)



# 获取模型结果
@app.post("/api/results")
async def get_results(request: ModelRequest):
    try:
        results = get_model_results(
            model=request.model,
            scene=request.scene,
            dataset_name=request.dataset_name
        )

        if results:
            return results
        else:
            raise HTTPException(status_code=500, detail="Error in generating results")

    except Exception as e:
        print(f"Error in API call: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# 获取规则信息的端点
@app.get("/api/rules/{dataset_name}")
async def get_rules(dataset_name: str):
    try:
        rules_data = load_rules_from_json(dataset_name)
        return {"rules_information": rules_data}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# 启动服务时运行
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
