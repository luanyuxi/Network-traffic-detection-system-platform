import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_APP_API_URL,  // 使用环境变量配置后端地址
});

export const login = (username, password) => {
  return api.post('/api/admin/login/access_token', new URLSearchParams({
    username,
    password,
  }));
};

// 其他 API 函数...


export const registerUser = (user) => {
  return api.post('/v1/user/register', user);
};

export const getUserInfo = (token) => {
  return api.get('/api/admin/login/getinfo', {
    headers: { Authorization: `Bearer ${token}` },
  });
};


