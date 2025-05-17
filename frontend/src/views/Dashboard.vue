<template>
  <div class="dashboard">
    <!-- 系统统计信息 -->
    <el-card class="stats-card">
      <h3>系统统计</h3>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card>总场景数：{{ stats.scenes }}</el-card>
        </el-col>
        <el-col :span="8">
          <el-card>总数据集数：{{ stats.datasets }}</el-card>
        </el-col>
        <el-col :span="8">
          <el-card>总模型数：{{ stats.models }}</el-card>
        </el-col>
      </el-row>
    </el-card>

    <!-- 地图和数据来源图表 -->
    <div class="charts-container">
      <!-- 地图展示 -->
      <el-card class="map-card">
        <h3>数据集分布地图</h3>
        <div id="map-chart" class="chart"></div>
      </el-card>

      <!-- 数据来源饼图 -->
      <el-card class="pie-card">
        <h3>数据来源</h3>
        <div id="pie-chart" class="chart"></div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';

export default {
  setup() {
    const stats = ref({
      scenes: 5,
      datasets: 12,
      models: 2,
    });

    const datasetInfo = {
      '韩国': ['car_baseline_1'],
      '澳大利亚': ['car_baseline_2', 'iot_baseline_1'],
      '中国': ['encrypt_thirdparty_1', 'encrypt_thirdparty_2', 'cloud_bupt_1', 'encrypt_baseline_1', 'mix_1'],
      '加拿大': ['iot_baseline_1'],
      '爱沙尼亚': ['iot_baseline_2'],
      '印度': ['iot_baseline_3', 'mix_2'],
    };

    const sourceInfo = [
      { name: '基础数据集', value: 7 },
      { name: '第三方数据集', value: 2 },
      { name: '极客数据集', value: 3 },
    ];

    onMounted(async () => {
      const response = await fetch('/src/assets/worldGeoJSON.json'); // 确保文件路径正确
      const worldGeoJSON = await response.json();

      echarts.registerMap('world', worldGeoJSON);
      initMapChart();
      initPieChart();
    });

    const initMapChart = () => {
      const mapChart = echarts.init(document.getElementById('map-chart'));
      mapChart.setOption({
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            const country = params.name;
            const datasets = datasetInfo[country];
            if (datasets && datasets.length > 0) {
              return `${country}<br>数据集: ${datasets.join(', ')}`;
            } else {
              return `${country}<br>无相关数据集`;
            }
          },
        },
        visualMap: {
          type: 'piecewise',
          orient: 'horizontal',  // 设置为水平排列
          bottom: 10,  // 将图例放到图表底部
          left: 'center',
          pieces: [
            { min: 2, label: '多个数据集', color: '#5B8FF9' },
            { min: 1, max: 1, label: '单个数据集', color: '#5AD8A6' },
          ],
        },
        series: [
          {
            name: '数据集分布',
            type: 'map',
            map: 'world',
            roam: true,
            emphasis: {
              label: { show: true },
            },
            data: Object.keys(datasetInfo).map((country) => ({
              name: country,
              value: datasetInfo[country].length,
            })),
          },
        ],
      });
    };

    const initPieChart = () => {
      const pieChart = echarts.init(document.getElementById('pie-chart'));
      pieChart.setOption({
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)',
        },
        series: [
          {
            name: '数据来源',
            type: 'pie',
            radius: '50%',
            label: {
              formatter: '{b}: {d}%', // 设置标签显示完整文字
              position: 'outside',
            },
            data: sourceInfo,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)',
              },
            },
          },
        ],
      });
    };

    return {
      stats,
      datasetInfo,
      sourceInfo,
    };
  },
};
</script>

<style scoped>
.dashboard {
  padding: 10px;
}

.stats-card {
  margin-bottom: 20px;
}

.charts-container {
  display: flex;
  gap: 20px;
}

.map-card,
.pie-card {
  flex: 1;
  min-width: 45%;
}

.chart {
  width: 100%;
  height: 350px;
}
</style>
