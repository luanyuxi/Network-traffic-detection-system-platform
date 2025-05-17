<template>
  <!-- 首页、登录页、注册页 不显示侧边栏和顶部 -->
  <div v-if="isPurePage">
    <router-view />
  </div>

  <!-- 其余页面使用完整布局 -->
  <el-container v-else style="height: 100vh;">
    <!-- 左侧导航栏 -->
    <el-aside width="200px" style="background-color: #2d3a4b;">
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        background-color="#2d3a4b"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <!-- 菜单项 -->
        <el-menu-item index="/dashboard" @click="navigateTo('/dashboard')">
          <i class="el-icon-s-home"></i>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/scene-dataset" @click="navigateTo('/scene-dataset')">
          <i class="el-icon-s-marketing"></i>
          <span>场景数据集选择</span>
        </el-menu-item>
        <el-menu-item index="/datasets" @click="navigateTo('/datasets')">
          <i class="el-icon-folder"></i>
          <span>数据集浏览</span>
        </el-menu-item>
        <el-menu-item index="/model-results" @click="navigateTo('/model-results')">
          <i class="el-icon-data-analysis"></i>
          <span>模型结果展示</span>
        </el-menu-item>
        <el-menu-item index="/rules-view" @click="navigateTo('/rules-view')">
          <i class="el-icon-document"></i>
          <span>规则展示及解释</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区域 -->
    <el-container>
      <el-header style="background-color: #333; color: #fff; display: flex; justify-content: space-between; align-items: center;">
        <!-- 面包屑导航 -->
        <el-breadcrumb separator="/" class="breadcrumb-custom">
          <el-breadcrumb-item @click.native="navigateTo('/dashboard')">首页</el-breadcrumb-item>
          <el-breadcrumb-item v-for="(item, index) in breadcrumbItems" :key="index">
            {{ item }}
          </el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 用户头像 -->
        <el-popover placement="bottom" width="200" trigger="hover">
          <template #reference>
            <div class="avatar-container">
              <el-avatar :src="avatarImage" class="avatar"></el-avatar>
            </div>
          </template>
          <div class="user-info">
            <p><strong>用户名：</strong> Leo_Ricap</p>
            <p><strong>生日：</strong> 2001/11/15</p>
          </div>
        </el-popover>
      </el-header>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import avatarImage from '@/assets/avatar.jpg';

export default {
  setup() {
    const router = useRouter();
    const route = useRoute();

    // 导航跳转
    const navigateTo = (path) => {
      router.push(path);
    };

    // 面包屑内容
    const breadcrumbItems = computed(() => {
      return route.matched.map((r) => r.meta.title).filter(Boolean);
    });

    // 判断是否为“纯页面”路由：首页、登录、注册页
    const isPurePage = computed(() =>
        ['/', '/login', '/signup'].includes(route.path)
    );

    return {
      navigateTo,
      breadcrumbItems,
      avatarImage,
      isPurePage,
    };
  },
};
</script>

<style scoped>
.el-menu-vertical-demo {
  height: 100%;
}

.breadcrumb-custom {
  color: #fff;
  padding: 10px;
  font-size: 16px;
}

.breadcrumb-custom .el-breadcrumb-item {
  color: #fff !important;
}

.breadcrumb-custom .el-breadcrumb__separator {
  color: #fff !important;
}

.avatar-container {
  cursor: pointer;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 20px;
}

.user-info p {
  margin: 0;
  font-size: 14px;
}
</style>
