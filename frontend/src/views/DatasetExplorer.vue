<template>
  <div>
    <h2>数据集浏览</h2>

    <el-form label-width="100px">
      <el-form-item label="选择场景">
        <el-select v-model="selectedScene" placeholder="请选择场景" @change="fetchDatasets">
          <el-option label="Car" value="car" />
          <el-option label="Encrypt" value="encrypt" />
          <el-option label="Cloud" value="cloud" />
          <el-option label="IoT" value="iot" />
          <el-option label="Mix" value="mix" />
        </el-select>
      </el-form-item>

      <el-form-item label="选择数据集">
        <el-select v-model="selectedDataset" placeholder="请选择数据集">
          <el-option v-for="dataset in datasets" :key="dataset" :label="dataset" :value="dataset" />
        </el-select>
      </el-form-item>

      <el-form-item label="上传文件">
        <el-upload
          action="/api/upload"
          :multiple="true"
          :file-list="fileList"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
        >
          <el-button size="small" type="primary">点击上传</el-button>
          <div slot="tip" class="el-upload__tip">只能上传数据文件</div>
        </el-upload>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const selectedScene = ref('');
    const selectedDataset = ref('');
    const datasets = ref([]);
    const fileList = ref([]);

    const fetchDatasets = () => {
      // 模拟根据场景获取数据集
      if (selectedScene.value === 'car') {
        datasets.value = ['car_baseline_1', 'car_baseline_2'];
      } else {
        datasets.value = [];
      }
    };

    const handlePreview = (file) => {
      console.log('预览文件', file);
    };

    const handleRemove = (file, fileList) => {
      console.log('移除文件', file, fileList);
    };

    return {
      selectedScene,
      selectedDataset,
      datasets,
      fileList,
      fetchDatasets,
      handlePreview,
      handleRemove,
    };
  },
};
</script>
