// /src/store/auth.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_APP_API_URL,
});

export default {
  namespaced: true, // 确保启用命名空间
  state: {
    token: localStorage.getItem('token') || '',
    userInfo: null,
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    setUserInfo(state, userInfo) {
      state.userInfo = userInfo;
    },
    clearAuthData(state) {
      state.token = '';
      state.userInfo = null;
      localStorage.removeItem('token');
    },
  },
  actions: {
    async login({ commit }, { username, password }) {
      try {
        const response = await api.post('/api/admin/login/access_token', new URLSearchParams({
          username,
          password,
        }));
        const token = response.data.access_token;
        commit('setToken', token);
        return true;
      } catch (error) {
        console.error('登录失败:', error);
        return false;
      }
    },
    async registerUser(_, user) {
      try {
        await api.post('/v1/user/register', user);
        return true;
      } catch (error) {
        console.error('注册失败:', error);
        return false;
      }
    },
    async fetchUserInfo({ commit, state }) {
      if (!state.token) return null;
      try {
        const response = await api.get('/api/admin/login/getinfo', {
          headers: { Authorization: `Bearer ${state.token}` },
        });
        commit('setUserInfo', response.data);
        return response.data;
      } catch (error) {
        console.error('获取用户信息失败:', error);
        return null;
      }
    },
    logout({ commit }) {
      commit('clearAuthData');
    },
  },
};
