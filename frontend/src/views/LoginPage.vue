<template>
  <div class="login-page">
    <div class="login-panel">
      <div class="login-title">🎯 平台登录</div>
      <el-form :model="form" @submit.native.prevent="handleLogin" label-position="top">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-button type="primary" class="login-btn" @click="handleLogin" round>登 录</el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const router = useRouter();

const form = reactive({
  username: '',
  password: ''
});

const handleLogin = async () => {
  try {
    const params = new URLSearchParams();
    params.append('username', form.username);
    params.append('password', form.password);

    const res = await axios.post('/api/admin/login/access_token', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });

    const token = res.data.access_token;
    localStorage.setItem('access_token', token); // 保存 token

    ElMessage.success('登录成功');
    router.push('/dashboard'); // ✅ 登录成功后跳转 dashboard

  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '登录失败');
  }
};
</script>


<style scoped>
.login-page {
  height: 100vh;
  background: #0e0f14;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-panel {
  background: #fff;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  width: 360px;
}

.login-title {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 20px;
}

.login-btn {
  width: 100%;
  margin-top: 10px;
}
</style>
