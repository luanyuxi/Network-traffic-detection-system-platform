// /src/store/data.js
export default {
  namespaced: true,
  state: {
    // 定义初始状态
    scenes: [],
    datasets: [],
  },
  mutations: {
    setScenes(state, scenes) {
      state.scenes = scenes;
    },
    setDatasets(state, datasets) {
      state.datasets = datasets;
    },
  },
  actions: {
    // 定义异步操作，例如从API加载数据
    async fetchScenes({ commit }) {
      const response = await getScenes(); // 确保导入了 getScenes API 函数
      commit('setScenes', response.data);
    },
    async fetchDatasets({ commit }, scene) {
      const response = await getDatasets(scene); // 确保导入了 getDatasets API 函数
      commit('setDatasets', response.data.datasets);
    },
  },
};
