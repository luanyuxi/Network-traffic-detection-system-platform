// /src/api/user.js
import axios from 'axios';
import.meta.env.VITE_APP_API_URL


const api = axios.create({
  baseURL: import.meta.env.VITE_APP_API_URL || 'http://localhost:5173', // 使用 import.meta.env 代替 process.env
});

// 获取当前登录用户的信息
export const getUserInfo = (token) => {
  return api.get('/api/admin/login/getinfo', {
    headers: { Authorization: `Bearer ${token}` },
  });
};
