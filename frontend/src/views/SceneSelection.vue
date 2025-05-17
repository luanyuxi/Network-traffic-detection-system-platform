<template>
  <div>
    <h2>场景选择</h2>
    <el-row :gutter="20">
      <el-col :span="4" v-for="scene in scenes" :key="scene">
        <el-card shadow="hover">
          <div slot="header" class="clearfix">
            <span>{{ scene }}</span>
          </div>
          <div>
            <el-button type="primary" @click="navigateToScene(scene)">
              进入{{ scene }}
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const scenes = ref(["Car", "Encrypt", "Cloud", "IoT", "Mix"]);
    const router = useRouter();

    const navigateToScene = (scene) => {
      router.push(`/scene/${scene.toLowerCase()}`);
    };

    return {
      scenes,
      navigateToScene,
    };
  },
};
</script>
