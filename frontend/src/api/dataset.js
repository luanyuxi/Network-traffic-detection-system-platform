import axios from 'axios';

// 获取特定场景的数据集
export const fetchDatasetsByScene = async (scene) => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_APP_API_URL}/api/datasets/${scene}`);
    return response.data.datasets; // 假设返回数据结构中有 datasets 列表
  } catch (error) {
    console.error("Error fetching datasets:", error);
    return [];
  }
};

// 获取特定数据集的详细信息
export const fetchDatasetDetails = async (dataset) => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_APP_API_URL}/api/dataset/${dataset}`);
    return response.data; // 假设返回的数据包含 description、features 和 labels
  } catch (error) {
    console.error("Error fetching dataset details:", error);
    return null;
  }
};
