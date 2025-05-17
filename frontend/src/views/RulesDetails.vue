<template>
  <div class="rules-details">
    <h2>规则详情</h2>
    <el-table :data="selectedRuleDetails" border style="width: 100%">
      <el-table-column prop="ruleIndex" label="规则编号" width="60" />
      <el-table-column
        v-for="feature in featureHeaders"
        :key="feature"
        :prop="feature"
        :label="feature"
        width="80"
      >
        <template #default="scope">
          <span class="small-text">[{{ scope.row[scope.column.property][0] }}, {{ scope.row[scope.column.property][1] }}]</span>
        </template>
      </el-table-column>
      <el-table-column prop="resultCondition" label="结果条件" width="120">
        <template #default="scope">
          <span class="small-text">{{ scope.row.resultCondition }}</span>
        </template>
      </el-table-column>
      <el-table-column label="规则展示" width="180">
        <template #default="scope">
          <el-tooltip class="item" effect="dark" content="点击查看完整规则" placement="top">
            <span @click="showFullRule(scope.row.ruleDisplay)" class="small-text clickable">
              {{ getShortRuleDisplay(scope.row.ruleDisplay) }}
            </span>
          </el-tooltip>
        </template>
      </el-table-column>
    </el-table>

    <!-- 规则展示的完整内容弹窗 -->
    <el-dialog title="完整规则展示" v-model="isDialogVisible" width="50%">
      <p>{{ fullRuleText }}</p>
      <span slot="footer" class="dialog-footer">
        <el-button @click="isDialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

export default {
  setup() {
    const route = useRoute();
    const dataset = route.query.dataset;
    const selectedRuleDetails = ref([]);
    const featureHeaders = ref([]);
    const isDialogVisible = ref(false);
    const fullRuleText = ref("");

    const getShortRuleDisplay = (ruleDisplay) => {
      const match = ruleDisplay.match(/If (x[0-9]+ .*? x[0-9]+).*then (.*)/i);
      return match ? `If ${match[1]} … then ${match[2]}` : ruleDisplay;
    };

    const loadRuleDetails = async () => {
      try {
        const response = await axios.get(`/api/rules/${dataset}`);
        const ruleInfo = response.data.rules_information;

        if (!ruleInfo || !ruleInfo.detailed_rules || ruleInfo.detailed_rules.length === 0) {
          console.warn(`数据集 "${dataset}" 没有详细规则信息。`);
          return;
        }

        featureHeaders.value = Object.keys(ruleInfo.detailed_rules[0].conditions);

        selectedRuleDetails.value = ruleInfo.detailed_rules.map((rule, index) => ({
          ruleIndex: index + 1,
          ...rule.conditions,
          resultCondition: rule.result,
          ruleDisplay: rule.rule_display
        }));
      } catch (error) {
        console.error("Error fetching rule details:", error);
      }
    };

    const showFullRule = (rule) => {
      fullRuleText.value = rule;
      isDialogVisible.value = true;
      console.log("Dialog visibility set to:", isDialogVisible.value);
    };

    onMounted(loadRuleDetails);

    return {
      selectedRuleDetails,
      featureHeaders,
      isDialogVisible,
      fullRuleText,
      getShortRuleDisplay,
      showFullRule
    };
  }
};
</script>

<style scoped>
.rules-details {
  padding: 20px;
}

.el-table th {
  font-size: 14px;
}

.small-text {
  font-size: 12px;
}

.clickable {
  color: #409EFF;
  cursor: pointer;
}

.el-table th, .el-table td {
  text-align: center;
  white-space: nowrap;
}
</style>
