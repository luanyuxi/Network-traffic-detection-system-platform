<!-- src/views/SignUpPage.vue -->
<template>
  <div class="signup-page">
    <el-card class="form-card">
      <h2 class="title">Create your account</h2>
      <el-form :model="form" label-position="top" @submit.native.prevent="handleSignup">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="form.confirm" type="password" placeholder="请再次输入密码" />
        </el-form-item>
        <el-button type="primary" class="submit-btn" @click="handleSignup">Sign Up</el-button>
        <el-divider>or</el-divider>
        <el-button type="text" @click="goLogin">Already have an account? Log In</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

const router = useRouter();
const form = reactive({ username: '', password: '', confirm: '' });

const handleSignup = () => {
  if (form.password !== form.confirm) {
    return ElMessage.error('两次密码输入不一致');
  }

  // 你可以在此调用注册 API，将用户名密码发送到后端
  ElMessage.success('注册成功，请登录');
  router.push('/login'); // ✅ 改这里
};

const goLogin = () => router.push('/login');
</script>


<style scoped>
.signup-page {
  min-height: 100vh;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}
.form-card {
  width: 360px;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}
.title {
  text-align: center;
  margin-bottom: 24px;
}
.submit-btn {
  width: 100%;
  margin-top: 10px;
}
</style>
