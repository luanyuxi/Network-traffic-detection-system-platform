<template>
  <el-dialog :visible.sync="visible" :title="datasetName + ' 详情'" width="60%">
    <el-card>
      <h3>数据集的描述</h3>
      <p>{{ datasetDescription }}</p>

      <h3>数据集的特征</h3>
      <el-table :data="datasetFeatures" border style="width: 100%">
        <el-table-column prop="name" label="特征" width="150"/>
        <el-table-column prop="description" label="说明"/>
      </el-table>

      <h3>数据集标签判定规则</h3>
      <p>{{ datasetLabelRules }}</p>
    </el-card>
    <span slot="footer" class="dialog-footer">
      <el-button @click="closeDialog">关闭</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      required: true,
    },
    datasetName: {
      type: String,
      required: true,
    },
    datasetDescription: {
      type: String,
      default: '',
    },
    datasetFeatures: {
      type: Array,
      default: () => [],
    },
    datasetLabelRules: {
      type: String,
      default: '',
    },
  },
  methods: {
    closeDialog() {
      this.$emit('update:visible', false);
    },
  },
};
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
