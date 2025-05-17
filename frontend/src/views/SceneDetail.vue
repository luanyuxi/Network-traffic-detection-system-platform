<template>
  <div>
    <h2>场景：{{ sceneName }}</h2>
    <el-row :gutter="20">
      <el-col :span="12" v-for="dataset in datasets" :key="dataset.name">
        <el-card>
          <h3>{{ dataset.name }}</h3>
          <p>{{ dataset.description }}</p>
          <el-button type="primary" @click="viewDatasetDetails(dataset.name)">
            查看详情
          </el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getDatasetsByScene } from '../api/dataset';

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const sceneName = ref(route.params.scene);
    const datasets = ref([]);

    onMounted(async () => {
      const scene = route.params.scene;
      const data = await getDatasetsByScene(scene); // 获取该场景下的数据集
      datasets.value = data.map((item) => ({
        name: item,
        description: `${scene}场景下的数据集 ${item}`,
      }));
    });

    const viewDatasetDetails = (datasetName) => {
      router.push(`/datasets/${datasetName}`);
    };

    return {
      sceneName,
      datasets,
      viewDatasetDetails,
    };
  },
};
</script>
