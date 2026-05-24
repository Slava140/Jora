<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCapabilitiesStore } from '@/stores/capabilities'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const caps = useCapabilitiesStore()

const activeMenu = computed(() => route.path.split('/')[1] || 'projects')

function logout() {
  caps.reset()
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <el-container class="layout">
    <el-aside width="220px" class="aside">
      <div class="logo">Jora</div>
      <el-menu :default-active="activeMenu" router>
        <el-menu-item index="projects" route="/projects">Проекты</el-menu-item>
        <el-menu-item index="tasks" route="/tasks">Задачи</el-menu-item>
        <el-menu-item v-if="caps.canManageUsers" index="users" route="/users">
          Пользователи
        </el-menu-item>
      </el-menu>
      <div class="aside-footer">
        <div class="user-name">{{ auth.user?.username }}</div>
        <el-button text type="danger" @click="logout">Выйти</el-button>
      </div>
    </el-aside>
    <el-main class="main">
      <slot />
    </el-main>
  </el-container>
</template>

<style scoped>
.layout {
  min-height: 100vh;
}
.aside {
  background: #1e293b;
  color: #fff;
  display: flex;
  flex-direction: column;
}
.logo {
  font-size: 1.5rem;
  font-weight: 700;
  padding: 1.25rem 1rem;
}
.aside :deep(.el-menu) {
  background: transparent;
  border: none;
  flex: 1;
}
.aside :deep(.el-menu-item) {
  color: #cbd5e1;
}
.aside :deep(.el-menu-item.is-active) {
  background: #334155;
  color: #fff;
}
.aside-footer {
  padding: 1rem;
  border-top: 1px solid #334155;
}
.user-name {
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  color: #94a3b8;
}
.main {
  background: #f8fafc;
  padding: 1.5rem 2rem;
}
</style>
