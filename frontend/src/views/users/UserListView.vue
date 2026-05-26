<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppShell from '@/components/layout/AppShell.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import * as usersApi from '@/api/users'
import { useAuthStore } from '@/stores/auth'
import { formatDisplayDatetime } from '@/utils/datetime'
import type { User } from '@/types'

const router = useRouter()
const auth = useAuthStore()

const users = ref<User[]>([])
const loading = ref(false)
const listUnavailable = ref(false)

async function load() {
  loading.value = true
  listUnavailable.value = false
  try {
    users.value = await usersApi.getUsers({ page: 1, limit: 100 })
  } catch {
    listUnavailable.value = true
    users.value = []
  } finally {
    loading.value = false
  }
}

function openProfile() {
  if (auth.user) {
    router.push(`/users/${auth.user.id}/edit`)
  }
}

onMounted(load)
</script>

<template>
  <AppShell>
    <PageHeader title="Пользователи">
      <template #actions>
        <el-button type="primary" @click="router.push('/users/new')">Создать</el-button>
      </template>
    </PageHeader>

    <el-alert
      v-if="listUnavailable"
      type="info"
      :closable="false"
      show-icon
      class="list-alert"
      title="Список пользователей недоступен на API. Вы можете создать пользователя или открыть свой профиль."
    />

    <div v-loading="loading" class="user-cards">
      <article
        v-for="user in users"
        :key="user.id"
        class="user-card jora-card"
        @click="router.push(`/users/${user.id}/edit`)"
      >
        <h3>{{ user.username }}</h3>
        <p class="email">{{ user.email }}</p>
        <footer>Создан {{ formatDisplayDatetime(user.create_datetime) }}</footer>
      </article>
    </div>

    <EmptyState
      v-if="!loading && users.length === 0"
      :title="listUnavailable ? 'Список недоступен' : 'Нет пользователей'"
      :description="
        listUnavailable
          ? 'Используйте кнопки ниже для управления.'
          : 'Создайте первого пользователя.'
      "
    >
      <el-button type="primary" @click="router.push('/users/new')">Создать пользователя</el-button>
      <el-button @click="openProfile">Мой профиль</el-button>
    </EmptyState>
  </AppShell>
</template>

<style scoped>
.list-alert {
  margin-bottom: 1rem;
}
.user-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}
.user-card {
  padding: 1rem 1.25rem;
  cursor: pointer;
  transition: box-shadow 0.15s;
}
.user-card:hover {
  box-shadow: 0 4px 12px rgba(9, 30, 66, 0.12);
}
.user-card h3 {
  margin: 0 0 0.25rem;
  font-size: 1rem;
}
.email {
  margin: 0 0 0.75rem;
  font-size: 0.875rem;
  color: var(--jora-text-muted);
}
footer {
  font-size: 0.75rem;
  color: var(--jora-text-muted);
}
</style>
