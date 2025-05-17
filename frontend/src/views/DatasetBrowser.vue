<template>
  <div class="dataset-browser">
    <el-card>
      <h2>数据集浏览</h2>

      <!-- 场景和数据集选择 -->
      <el-form label-width="90px" style="margin-bottom: 20px; width: 100%;">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="选择场景">
              <el-select v-model="selectedScene" placeholder="选择场景" @change="updateDatasets" style="width: 100%;">
                <el-option v-for="scene in scenes" :key="scene" :label="scene" :value="scene" />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="选择数据集">
              <el-select v-model="selectedDataset" placeholder="选择数据集" @change="fetchDatasetContents" style="width: 100%;">
                <el-option v-for="dataset in filteredDatasets" :key="dataset" :label="dataset" :value="dataset" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <!-- 数据集内容表格展示 -->
      <div v-if="datasetContents">
        <el-card>
          <h3>数据集内容</h3>
          <el-table :data="tableData" border style="width: 100%">
            <el-table-column type="index" label="序号" width="60"></el-table-column>
            <el-table-column prop="filename" label="文件名" />
            <el-table-column prop="path" label="描述（路径）" />
            <el-table-column prop="creationTime" label="创建时间" />
            <el-table-column label="操作" align="center">
              <template #default="scope">
                <div class="operation-links">
                  <el-link type="primary" @click="downloadFile(scope.row.downloadLink)" underline>下载</el-link>
                  <el-link type="warning" @click="modifyFile(scope.row.filename)" underline>修改</el-link>
                  <el-link type="danger" @click="deleteFile(scope.row.filename)" underline>删除</el-link>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import axios from "axios";

export default {
  setup() {
    // 场景固定
    const scenes = ref(["Car", "Encrypt", "Cloud", "IoT", "Mix"]);

    // 数据集列表由后端动态加载
    const datasets = ref([]);

    // 选中的场景和数据集
    const selectedScene = ref("");
    const selectedDataset = ref("");

    // 数据集内容和表格数据
    const datasetContents = ref(null);
    const tableData = ref([]);

    // 过滤：不区分大小写，匹配前缀
    const filteredDatasets = computed(() =>
      datasets.value.filter((dataset) =>
        dataset.toLowerCase().startsWith(selectedScene.value.toLowerCase())
      )
    );

    // 选择场景后，动态获取该场景下的数据集
    const updateDatasets = async () => {
      selectedDataset.value = "";
      datasetContents.value = null;
      tableData.value = [];

      if (selectedScene.value) {
        try {
          const res = await axios.get(`http://127.0.0.1:8000/api/datasets/${selectedScene.value}`);
          datasets.value = res.data.datasets;
        } catch (err) {
          console.error("获取数据集失败:", err);
          datasets.value = [];
        }
      }
    };

    // 加载选中数据集的文件列表
    const fetchDatasetContents = async () => {
      if (selectedDataset.value) {
        try {
          const response = await axios.get(`http://127.0.0.1:8000/api/dataset/${selectedDataset.value}`);
          datasetContents.value = response.data;

          tableData.value = Object.keys(datasetContents.value).map((filename) => ({
            filename,
            path: `/backend/models/${selectedDataset.value}/data/${filename}`,
            downloadLink: `http://127.0.0.1:8000/api/dataset/${selectedDataset.value}/file/${filename}`,
            creationTime: new Date().toISOString().slice(0, 19).replace("T", " ")
          }));
        } catch (error) {
          console.error("获取数据集内容失败:", error);
        }
      }
    };

    // 下载操作
    const downloadFile = (url) => {
      window.open(url, "_blank");
    };

    // 预留功能
    const modifyFile = (filename) => {
      console.log(`修改文件: ${filename}`);
    };

    const deleteFile = (filename) => {
      console.log(`删除文件: ${filename}`);
    };

    return {
      scenes,
      selectedScene,
      selectedDataset,
      datasets,
      filteredDatasets,
      datasetContents,
      tableData,
      updateDatasets,
      fetchDatasetContents,
      downloadFile,
      modifyFile,
      deleteFile
    };
  },
};
</script>


<style scoped>
.dataset-browser {
  padding: 20px;
}

.dataset-details {
  margin-top: 20px;
}

.operation-links {
  display: flex;
  justify-content: center;
  gap: 10px;
  font-size: 14px;
}

.el-table th,
.el-table td {
  padding: 12px !important;
}
</style>
