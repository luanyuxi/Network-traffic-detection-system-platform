<template>
  <div>
    <el-select v-model="selectedScene" placeholder="选择场景">
      <el-option v-for="scene in scenes" :key="scene" :label="scene" :value="scene" />
    </el-select>
    <el-table :data="datasets" style="width: 100%">
      <el-table-column prop="name" label="数据集名称" />
    </el-table>
  </div>
</template>

<script>
import {getDatasets} from '../api/dataset';

export default {
  props: ['scenes'],
  data() {
    return {
      datasets: [],
      selectedScene: null,
    };
  },
  watch: {
    async selectedScene(newScene) {
      const response = await getDatasets(newScene);
      this.datasets = response.data.datasets;
    },
  },
};
</script>
