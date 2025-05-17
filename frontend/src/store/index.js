// /src/store/index.js
import { createStore } from 'vuex';
import auth from './auth'; // 确保 auth.js 模块存在并导出
import data from './data'; // 确保 data.js 模块正确导出

export default createStore({
  modules: {
    auth,
    data, // 确保这里使用的是模块对象
  },
});
