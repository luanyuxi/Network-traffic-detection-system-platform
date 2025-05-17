<!-- src/views/Login.vue -->
<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>用户登录</h2>
      <el-form :model="form" @submit.native.prevent="handleLogin">
        <el-form-item label="用户名">
          <el-input v-model="form.username" autocomplete="off" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" autocomplete="off" />
        </el-form-item>
        <el-button type="primary" @click="handleLogin" style="width: 100%;">登录</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

const form = reactive({
  username: "",
  password: ""
});

const handleLogin = async () => {
  try {
    const params = new URLSearchParams();
    params.append("username", form.username);
    params.append("password", form.password);

    const res = await axios.post("http://127.0.0.1:8000/api/admin/login/access_token", params, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
    });

    const token = res.data.access_token;
    localStorage.setItem("access_token", token);
    alert("登录成功！");
    router.push("/home"); // 登录后跳转页面
  } catch (err) {
    alert("登录失败：" + (err.response?.data?.detail || "未知错误"));
  }
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
.login-card {
  width: 400px;
  padding: 20px;
}
</style>
