const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// 定义数据集的基础路径，比如 backend/models/
const DATASETS_BASE_PATH = path.join(__dirname, 'models');

// 定义 API 路径：获取指定数据集的文件内容
app.get('/api/dataset/:datasetName', (req, res) => {
  const { datasetName } = req.params;
  const datasetPath = path.join(DATASETS_BASE_PATH, datasetName, 'data');

  // 检查路径是否存在
  if (!fs.existsSync(datasetPath)) {
    return res.status(404).json({ error: 'Dataset not found' });
  }

  // 读取 `data` 文件夹中的所有文件
  fs.readdir(datasetPath, (err, files) => {
    if (err) {
      return res.status(500).json({ error: 'Error reading dataset files' });
    }

    const fileContents = {};

    // 读取每个文件的内容并存储在 `fileContents` 对象中
    files.forEach((file) => {
      const filePath = path.join(datasetPath, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      fileContents[file] = content;
    });

    // 返回所有文件的内容
    res.json(fileContents);
  });
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
