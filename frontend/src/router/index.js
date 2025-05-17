import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import LoginPage from '@/views/LoginPage.vue';
import SignUpPage from '@/views/SignUpPage.vue';

import Dashboard from '@/views/Dashboard.vue';
import DatasetBrowser from '@/views/DatasetBrowser.vue';
import SceneDatasetSelection from '@/views/SceneDatasetSelection.vue';
import ModelResults from '@/views/ModelResults.vue';
import RulesView from '@/views/RulesView.vue';
import RulesDetails from '@/views/RulesDetails.vue';
import ExplanationView from '@/views/ExplanationView.vue';


const routes = [
  // 登录模块
  { path: '/', name: 'Home', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/signup', component: SignUpPage },
  { path: '/dashboard', component: Dashboard },

  // 系统功能模块
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { title: '仪表盘' },
  },
  {
    path: '/scene-dataset',
    name: 'SceneDatasetSelection',
    component: SceneDatasetSelection,
    meta: { title: '场景数据集选择' },
  },
  {
    path: '/datasets',
    name: 'DatasetBrowser',
    component: DatasetBrowser,
    meta: { title: '数据集浏览' },
  },
  {
    path: '/model-results',
    name: 'ModelResults',
    component: ModelResults,
    meta: { title: '模型结果展示' },
  },
  {
    path: '/rules-view',
    name: 'RulesView',
    component: RulesView,
    meta: { title: '规则展示及解释' },
  },
  {
    path: '/rules-details',
    name: 'RulesDetails',
    component: RulesDetails,
    meta: { title: '规则详情' },
  },
  {
    path: '/rules-explanation',
    name: 'ExplanationView',
    component: ExplanationView,
    meta: { title: '规则解释' },
    props: (route) => ({ dataset: route.query.dataset }),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_APP_API_URL),
  routes,
});

export default router;
