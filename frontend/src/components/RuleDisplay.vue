<template>
  <div>
    <h3>规则详情</h3>
    <p>规则数量：{{ rules.length }}</p>
    <el-table :data="rules" style="width: 100%">
      <el-table-column prop="rule" label="规则" />
      <el-table-column prop="description" label="描述" />
    </el-table>
  </div>
</template>

<script>
export default {
  props: ['rules'],
};
</script>
