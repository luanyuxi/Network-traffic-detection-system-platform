<template>
  <div>
    <h3>t-SNE 可视化</h3>
    <div ref="tsneChart" style="width: 100%; height: 400px;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  props: ['coordinates'],
  mounted() {
    this.initChart();
  },
  methods: {
    initChart() {
      const chart = echarts.init(this.$refs.tsneChart);
      const data = this.coordinates.map(coord => ({
        value: [coord.x, coord.y],
      }));

      const option = {
        xAxis: {},
        yAxis: {},
        series: [
          {
            type: 'scatter',
            data,
          },
        ],
      };

      chart.setOption(option);
    },
  },
};
</script>
