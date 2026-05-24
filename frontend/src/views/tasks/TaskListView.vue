<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppLayout from '@/components/AppLayout.vue'
import PaginationBar from '@/components/PaginationBar.vue'
import TaskFilters from '@/components/TaskFilters.vue'
import * as tasksApi from '@/api/tasks'
import * as projectsApi from '@/api/projects'
import * as usersApi from '@/api/users'
import { formatDisplayDatetime } from '@/utils/datetime'
import { getErrorMessage } from '@/utils/errors'
import type { Project, TaskFilters as TFilters, TaskWithMedia, User } from '@/types'

const router = useRouter()

const tasks = ref<TaskWithMedia[]>([])
const projects = ref<Project[]>([])
const users = ref<User[]>([])
const loading = ref(false)
const page = ref(1)
const limit = ref(10)

const filters = ref<TFilters>({ page: 1, limit: 10 })

const statusLabels: Record<string, string> = {
  open: 'Открыта',
  in_progress: 'В работе',
  finished: 'Завершена',
}

async function loadRefs() {
  const [p, u] = await Promise.all([
    projectsApi.getProjects({ page: 1, limit: 100 }),
    usersApi.getUsers({ page: 1, limit: 100 }),
  ])
  projects.value = p
  users.value = u
}

async function load() {
  if (
    (filters.value.from && !filters.value.to) ||
    (!filters.value.from && filters.value.to)
  ) {
    return
  }
  loading.value = true
  try {
    tasks.value = await tasksApi.getTasks({
      ...filters.value,
      page: page.value,
      limit: limit.value,
    })
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadRefs()
  await load()
})
</script>

<template>
  <AppLayout>
    <div class="page-header">
      <h1>Задачи</h1>
      <el-button type="primary" @click="router.push('/tasks/new')">Создать задачу</el-button>
    </div>

    <TaskFilters v-model="filters" :projects="projects" :users="users" @apply="load" />

    <el-table
      v-loading="loading"
      :data="tasks"
      stripe
      @row-click="(row: TaskWithMedia) => router.push(`/tasks/${row.id}`)"
    >
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="title" label="Название" />
      <el-table-column label="Проект" width="100">
        <template #default="{ row }">#{{ row.project_id }}</template>
      </el-table-column>
      <el-table-column label="Статус" width="120">
        <template #default="{ row }">{{ statusLabels[row.status] ?? row.status }}</template>
      </el-table-column>
      <el-table-column label="Срок">
        <template #default="{ row }">{{ formatDisplayDatetime(row.due_date) }}</template>
      </el-table-column>
      <el-table-column label="Исполнитель" width="110">
        <template #default="{ row }">{{ row.assignee_id ?? '—' }}</template>
      </el-table-column>
    </el-table>

    <PaginationBar v-model:page="page" v-model:limit="limit" @change="load" />
  </AppLayout>
</template>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.page-header h1 {
  margin: 0;
}
:deep(.el-table__row) {
  cursor: pointer;
}
</style>
