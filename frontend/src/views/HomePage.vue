<template>
  <div class="home-page">
    <!-- 顶部导航 -->
    <header class="hero-header">
      <img :src="logo" alt="Nexora Logo" class="logo-image" />
      <nav>
        <el-button type="text" @click="showPricing = true" style="color: white;">Pricing</el-button>
        <el-button type="text" @click="goLogin" style="color: white;">Log In</el-button>
        <el-button type="primary" @click="goSignup">Sign Up</el-button>
      </nav>
    </header>

    <!-- Hero 内容 -->
    <section class="hero-content">
      <h1>where creativity<br/>meets productivity</h1>
      <p>Real-time traffic awareness. Powered by Nexora.</p>
      <div class="hero-actions">
        <el-button size="large" type="primary" @click="goSignup">Try Clover for Free</el-button>

      </div>
    </section>

    <!-- Pricing 弹窗修复后写法 -->
    <el-dialog title="Pricing" v-model="showPricing" width="400px">
      <div>当然是免费的啦 🎉</div>
      <template #footer>
        <el-button @click="showPricing = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {ref} from 'vue';
import {useRouter} from 'vue-router';
import logo from '@/assets/logo.png';

const showPricing = ref(false);
const router = useRouter();


const goLogin = () => router.push('/login');
const goSignup = () => router.push('/signup');
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #0e0f14;
  color: #fff;
  display: flex;
  flex-direction: column;
}
.logo-container {
  display: flex;
  align-items: center;
  font-size: 4px;
  font-weight: bold;
  color: white;
}

.logo-img {
  height: 1px;
  margin-right: 2px;
}

.hero-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 60px;
}
.hero-header .logo {
  font-size: 48px;
  font-weight: bold;
}
.hero-header nav > * {
  margin-left: 20px;
}

.hero-content {
  flex: 1;
  text-align: center;
  padding: 80px 40px;
}
.hero-content h1 {
  font-size: 128px;
  font-weight: bold;
  line-height: 1.2;
  margin-bottom: 10px;

  background: linear-gradient(90deg, #ff3cac, #784ba0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-content p {
  font-size: 36px;
  margin-bottom: 64px;
  color: #ccc;
}
.hero-actions el-button {
  margin: 0 20px;
}
</style>
