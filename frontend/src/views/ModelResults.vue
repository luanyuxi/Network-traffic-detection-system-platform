<template>
  <div class="model-results">
    <el-form label-width="120px">
      <!-- 场景选择 -->
      <el-form-item label="选择场景">
        <el-select v-model="selectedScene" placeholder="选择场景" @change="updateDatasets">
          <el-option v-for="scene in scenes" :key="scene" :label="scene" :value="scene" />
        </el-select>
      </el-form-item>
      <!-- 数据集选择 -->
      <el-form-item label="选择数据集">
        <el-select v-model="selectedDataset" placeholder="选择数据集">
          <el-option v-for="dataset in datasets" :key="dataset" :label="dataset" :value="dataset" />
        </el-select>
      </el-form-item>
      <!-- 模型算法选择 -->
      <el-form-item label="选择模型算法">
        <el-select v-model="selectedModel" placeholder="选择模型算法">
          <el-option label="XGBoost" value="xgboost" />
          <el-option label="Random Forest" value="randomforest" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="fetchResults">运行</el-button>
      </el-form-item>
    </el-form>

    <div v-if="metricsData">
      <!-- 结果展示区域，使用四个指标的对比柱状图 -->
      <h3>模型指标对比</h3>
      <canvas id="metrics-bar-chart"></canvas>

      <!-- t-SNE 散点图 -->
      <h3>t-SNE 散点图</h3>
      <canvas id="tsne-scatter-chart"></canvas>
    </div>
  </div>
</template>

<script>
import {ref, nextTick} from "vue";
import axios from "axios";
import {fetchDatasetsByScene} from "@/api/dataset";
import {
  Chart,
  BarController,
  BarElement,
  ScatterController,
  PointElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from "chart.js";

// 注册 Chart.js 所需组件
Chart.register(BarController, BarElement, ScatterController, PointElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

export default {
  setup() {
    const scenes = ref(["Car", "Encrypt", "Cloud", "IoT", "Mix"]);
    const datasets = ref([]);
    const selectedScene = ref("");
    const selectedDataset = ref("");
    const selectedModel = ref("");
    const metricsData = ref(null);
    const tsneData = ref(null);
    const selectedClusters = ref([]);

    // 用于存储 Chart 实例
    let barChartInstance = null;
    let scatterChartInstance = null;

    const updateDatasets = async () => {
      if (selectedScene.value) {
        try {
          datasets.value = await fetchDatasetsByScene(selectedScene.value);
          console.log("返回的数据集列表:", datasets.value);
        } catch (error) {
          console.error("加载数据集时出错:", error);
        }
      } else {
        datasets.value = [];
      }
    };

    const fetchResults = async () => {
      try {
        const response = await axios.get(`/api/results/${selectedModel.value}/${selectedScene.value}/${selectedDataset.value}`);
        const data = response.data;

        const modelKey = selectedModel.value === 'xgboost' ? 'XGBoost' : 'Random Forest';

        if (!data.models || !data.models[modelKey]) {
          console.warn("No data found for model key:", modelKey);
          console.warn("Available keys in models:", Object.keys(data.models || {}));
          return;
        }

        metricsData.value = data.models[modelKey];
        tsneData.value = data.tsne_coordinates;
        selectedClusters.value = data.selected_clusters;

        if (metricsData.value && tsneData.value) {
          await nextTick(); // 确保 DOM 渲染完毕
          drawCharts();
        } else {
          console.warn("No metrics or t-SNE data found in the response.");
        }
      } catch (error) {
        console.error("Error fetching results:", error);
      }
    };

    const drawCharts = () => {
      if (!metricsData.value || !tsneData.value) {
        console.warn("metricsData 或 tsneData 没有数据，无法绘制图表。");
        return;
      }

      // 销毁之前的 Chart 实例
      if (barChartInstance) {
        barChartInstance.destroy();
      }
      if (scatterChartInstance) {
        scatterChartInstance.destroy();
      }

      // 绘制柱状图
      const ctxBar = document.getElementById("metrics-bar-chart").getContext("2d");
      barChartInstance = new Chart(ctxBar, {
        type: 'bar',
        data: {
          labels: ["Accuracy", "Precision", "Recall", "F1-score"],
          datasets: [
            {
              label: "Without Rules",
              data: [
                metricsData.value.without_rules.Accuracy,
                metricsData.value.without_rules.precision,
                metricsData.value.without_rules.recall,
                metricsData.value.without_rules["f1-score"]
              ],
              backgroundColor: "rgba(75, 192, 192, 0.5)",
              borderColor: "rgba(75, 192, 192, 1)"
            },
            {
              label: "With Rules",
              data: [
                metricsData.value.with_rules.Accuracy,
                metricsData.value.with_rules.precision,
                metricsData.value.with_rules.recall,
                metricsData.value.with_rules["f1-score"]
              ],
              backgroundColor: "rgba(153, 102, 255, 0.5)",
              borderColor: "rgba(153, 102, 255, 1)"
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {position: 'top'},
            title: {display: true, text: '模型指标对比'}
          }
        }
      });

      // 绘制 t-SNE 散点图
      const ctxScatter = document.getElementById("tsne-scatter-chart").getContext("2d");
      scatterChartInstance = new Chart(ctxScatter, {
        type: 'scatter',
        data: {
          datasets: selectedClusters.value.map((cluster, index) => ({
            label: `Cluster ${cluster}`,
            data: tsneData.value
                .filter(point => point.Cluster === cluster)
                .map(point => ({
                  x: point["t-SNE Feature 1"],
                  y: point["t-SNE Feature 2"]
                })),
            backgroundColor: `hsl(${(index / selectedClusters.value.length) * 360}, 100%, 50%)`
          }))
        },
        options: {
          scales: {
            x: {title: {display: true, text: 't-SNE Feature 1'}},
            y: {title: {display: true, text: 't-SNE Feature 2'}}
          },
          plugins: {
            title: {display: true, text: 't-SNE 散点图'}
          }
        }
      });
    };

    return {
      scenes,
      datasets,
      selectedScene,
      selectedDataset,
      selectedModel,
      updateDatasets,
      fetchResults,
      metricsData,
      tsneData,
      selectedClusters
    };
  },
};
</script>

<style scoped>
.model-results {
  padding: 20px;
}
</style>
