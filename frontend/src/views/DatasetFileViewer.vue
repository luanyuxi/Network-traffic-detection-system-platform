<template>
  <div>
    <h2>数据集文件内容</h2>
    <el-table :data="fileData" style="width: 100%">
      <el-table-column v-for="column in columns" :key="column" :prop="column" :label="column" />
    </el-table>
  </div>
</template>

<script>
import { getFileContent } from '../api/dataset';

export default {
  props: ['scene', 'dataset', 'file'],
  data() {
    return {
      columns: [],
      fileData: [],
    };
  },
  async created() {
    const response = await getFileContent(this.scene, this.dataset, this.file);
    this.fileData = response.data.rows;
    this.columns = response.data.columns;
  },
};
</script>
