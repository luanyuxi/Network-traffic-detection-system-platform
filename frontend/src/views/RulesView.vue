<template>
  <div class="rules-view">
    <h2>规则展示</h2>
    <el-table :data="rulesList" border style="width: auto; min-width: 100%;" :fit="true">
      <el-table-column prop="index" label="序号" min-width="50" />
      <el-table-column prop="datasetName" label="规则名称" min-width="150" />
      <el-table-column prop="ruleCount" label="规则数量" min-width="100" />

      <!-- 模型选择部分 -->
      <el-table-column label="模型选择" min-width="180">
        <template #default="scope">
          <span
            class="model-choice"
            :class="{ selected: scope.row.selectedModel === 'xgboost' }"
            @click="selectModel(scope.row, 'xgboost')"
          >
            XGBoost
          </span>
          <span
            class="model-choice"
            :class="{ selected: scope.row.selectedModel === 'randomforest' }"
            @click="selectModel(scope.row, 'randomforest')"
          >
            Random Forest
          </span>
        </template>
      </el-table-column>

      <!-- 操作部分 -->
      <el-table-column label="操作" min-width="120">
        <template #default="scope">
          <span class="operation-link" @click="viewRuleDetails(scope.row)">
            查看规则
          </span>
          <span class="operation-link" @click="viewExplanation(scope.row)">
            查看解释
          </span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();
    const rulesList = ref([]);

    // 加载规则列表
    const loadRulesList = async () => {
      const datasets = [
        "car_baseline_1", "car_baseline_2", "cloud_baseline_1", "cloud_bupt_1",
        "encrypt_baseline_1", "encrypt_thirdparty_1", "encrypt_thirdparty_2",
        "iot_baseline_1", "iot_baseline_2", "iot_baseline_3", "mix_1", "mix_2"
      ];
      rulesList.value = await Promise.all(datasets.map(async (dataset, index) => {
        const response = await axios.get(`/api/rules/${dataset}`);
        return {
          index: index + 1,
          datasetName: dataset,
          ruleCount: response.data.rules_information.number_of_rules,
          selectedModel: null,
          dataset: dataset
        };
      }));
    };

    // 选择模型
    const selectModel = (row, model) => {
      row.selectedModel = model;
    };

    // 查看详细规则，跳转到新页面
    const viewRuleDetails = (row) => {
      router.push({ path: '/rules-details', query: { dataset: row.dataset } });
    };

    // 查看解释的功能
    const viewExplanation = (row) => {
      router.push({ path: '/rules-explanation', query: { dataset: row.dataset } });
    };

    loadRulesList();

    return {
      rulesList,
      selectModel,
      viewRuleDetails,
      viewExplanation
    };
  }
};
</script>

<style scoped>
.rules-view {
  padding: 20px;
}

/* 自定义模型选择的样式 */
.model-choice {
  color: #409EFF;
  cursor: pointer;
  margin-right: 10px;
}

.model-choice.selected {
  font-weight: bold;
  color: #67C23A; /* 选中状态为绿色 */
}

/* 自定义操作链接的样式 */
.operation-link {
  color: #409EFF;
  cursor: pointer;
  margin-right: 10px;
}

/* 设置表格内容适应宽度 */
.el-table-column {
  white-space: nowrap; /* 防止内容换行 */
}
</style>
