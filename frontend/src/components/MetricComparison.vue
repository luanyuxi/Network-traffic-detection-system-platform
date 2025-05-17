<template>
  <div>
    <h3>指标对比</h3>
    <el-table :data="metricsData">
      <el-table-column prop="type" label="模型类型" />
      <el-table-column prop="accuracy" label="准确率" />
      <el-table-column prop="precision" label="精确率" />
      <el-table-column prop="recall" label="召回率" />
      <el-table-column prop="f1_score" label="F1得分" />
    </el-table>
  </div>
</template>

<script>
export default {
  props: ['metrics'],
  computed: {
    metricsData() {
      return [
        {
          type: '有规则',
          ...this.metrics.with_rules,
        },
        {
          type: '无规则',
          ...this.metrics.without_rules,
        },
      ];
    },
  },
};
</script>
