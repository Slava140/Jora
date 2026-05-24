<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppLayout from '@/components/AppLayout.vue'
import * as projectsApi from '@/api/projects'
import * as tasksApi from '@/api/tasks'
import { useAuthStore } from '@/stores/auth'
import { formatDisplayDatetime } from '@/utils/datetime'
import { downloadBlob } from '@/utils/blob'
import { getErrorMessage } from '@/utils/errors'
import type { Project, TaskWithMedia } from '@/types'

const props = defineProps<{ id: string }>()
const router = useRouter()
const auth = useAuthStore()

const canEditProject = computed(
  () => project.value !== null && project.value.owner_id === auth.user?.id,
)

const projectId = computed(() => parseInt(props.id, 10))
const project = ref<Project | null>(null)
const tasks = ref<TaskWithMedia[]>([])
const loading = ref(false)

const statusLabels: Record<string, string> = {
  open: 'Открыта',
  in_progress: 'В работе',
  finished: 'Завершена',
}

async function load() {
  loading.value = true
  try {
    project.value = await projectsApi.getProjectById(projectId.value)
    tasks.value = await tasksApi.getTasks({
      project_id: projectId.value,
      page: 1,
      limit: 50,
    })
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
    router.push('/projects')
  } finally {
    loading.value = false
  }
}

async function exportProject() {
  try {
    const blob = await projectsApi.exportProject(projectId.value)
    downloadBlob(blob, 'project.json')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  }
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div v-loading="loading">
      <div class="page-header" v-if="project">
        <div>
          <h1>{{ project.title }}</h1>
          <p class="desc">{{ project.description || 'Без описания' }}</p>
          <p class="meta">
            Создан: {{ formatDisplayDatetime(project.created_at) }} · Владелец #{{ project.owner_id }}
          </p>
        </div>
        <div class="actions">
          <el-button @click="router.push(`/tasks/new?project_id=${projectId}`)">Новая задача</el-button>
          <el-button @click="exportProject">Экспорт JSON</el-button>
          <template v-if="canEditProject">
            <el-button @click="router.push(`/projects/${projectId}/edit`)">Редактировать</el-button>
          </template>
          <el-button @click="router.push('/projects')">Назад</el-button>
        </div>
      </div>

      <h2>Задачи проекта</h2>
      <el-table :data="tasks" stripe @row-click="(row: TaskWithMedia) => router.push(`/tasks/${row.id}`)">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="Название" />
        <el-table-column label="Статус">
          <template #default="{ row }">{{ statusLabels[row.status] ?? row.status }}</template>
        </el-table-column>
        <el-table-column label="Исполнитель">
          <template #default="{ row }">{{ row.assignee_id ?? '—' }}</template>
        </el-table-column>
        <el-table-column label="Медиа" width="80">
          <template #default="{ row }">{{ row.media?.length ?? 0 }}</template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!loading && tasks.length === 0" description="Нет задач" />
    </div>
  </AppLayout>
</template>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  gap: 1rem;
}
.page-header h1 {
  margin: 0;
}
.desc {
  color: #475569;
  margin: 0.5rem 0;
}
.meta {
  font-size: 0.875rem;
  color: #64748b;
}
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: flex-start;
}
h2 {
  margin: 0 0 1rem;
}
:deep(.el-table__row) {
  cursor: pointer;
}
</style>
