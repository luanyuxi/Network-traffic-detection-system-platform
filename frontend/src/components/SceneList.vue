<template>
  <div>
    <el-table :data="scenes" style="width: 100%">
      <el-table-column prop="name" label="场景名称" />
    </el-table>
  </div>
</template>

<script>
import { getScenes } from '../api/scenes';

export default {
  data() {
    return {
      scenes: [],
    };
  },
  async created() {
    const response = await getScenes();
    this.scenes = response.data;
  },
};
</script>
