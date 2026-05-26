<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCapabilitiesStore } from '@/stores/capabilities'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const caps = useCapabilitiesStore()

const activeNav = computed(() => {
  if (route.path.startsWith('/my-tasks')) return 'my-tasks'
  return 'projects'
})

function logout() {
  caps.reset()
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="topbar-left">
        <router-link to="/projects" class="logo">Jora</router-link>
        <nav class="nav">
          <router-link
            to="/projects"
            class="nav-link"
            :class="{ active: activeNav === 'projects' }"
          >
            Проекты
          </router-link>
          <router-link
            to="/my-tasks"
            class="nav-link"
            :class="{ active: activeNav === 'my-tasks' }"
          >
            Мои задачи
          </router-link>
        </nav>
      </div>
      <div class="topbar-right">
        <span class="username">{{ auth.user?.username }}</span>
        <el-button text type="danger" @click="logout">Выйти</el-button>
      </div>
    </header>
    <main class="main">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  height: 56px;
  background: var(--jora-surface);
  border-bottom: 1px solid var(--jora-border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.topbar-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}
.logo {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--jora-primary);
  text-decoration: none;
}
.logo:hover {
  text-decoration: none;
  color: var(--jora-primary-hover);
}
.nav {
  display: flex;
  gap: 0.25rem;
}
.nav-link {
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  color: var(--jora-text-muted);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
}
.nav-link:hover {
  background: var(--jora-bg);
  color: var(--jora-text);
  text-decoration: none;
}
.nav-link.active {
  color: var(--jora-primary);
  background: #deebff;
}
.topbar-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.username {
  font-size: 0.875rem;
  color: var(--jora-text-muted);
}
.main {
  flex: 1;
  padding: 1.5rem 2rem;
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
}
</style>
