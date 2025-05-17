// /src/api/model.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_APP_API_URL,  // 使用环境变量配置后端地址
});

export const getModelResults = (model, scene, datasetName) => {
  return api.post('/api/results', {
    model,
    scene,
    dataset_name: datasetName,
  });
};
