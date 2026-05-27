<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppShell from '@/components/layout/AppShell.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import TaskKanban from '@/components/tasks/TaskKanban.vue'
import * as projectsApi from '@/api/projects'
import * as tasksApi from '@/api/tasks'
import { useAuthStore } from '@/stores/auth'
import { downloadBlob } from '@/utils/blob'
import { getErrorMessage } from '@/utils/errors'
import type { Project, TaskStatus, TaskWithMedia, User } from '@/types'

const props = defineProps<{ projectId: string }>()
const router = useRouter()
const auth = useAuthStore()

const id = computed(() => parseInt(props.projectId, 10))
const project = ref<Project | null>(null)
const tasks = ref<TaskWithMedia[]>([])
const projectUsers = ref<User[]>([])
const loading = ref(false)

const canEditProject = computed(
  () => project.value !== null && project.value.owner_id === auth.user?.id,
)

const usersMap = computed(() =>
  Object.fromEntries(projectUsers.value.map((u) => [u.id, u.username])),
)

async function load() {
  loading.value = true
  try {
    const [p, t, u] = await Promise.all([
      projectsApi.getProjectById(id.value),
      tasksApi.getTasks({ project_id: id.value, page: 1, limit: 100 }),
      projectsApi.getProjectUsers(id.value),
    ])
    project.value = p
    tasks.value = t
    projectUsers.value = u
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
    router.push('/projects')
  } finally {
    loading.value = false
  }
}

async function onDropTask(taskId: number, newStatus: TaskStatus) {
  const task = tasks.value.find((t) => t.id === taskId)
  if (!task || task.status === newStatus) return

  const prevStatus = task.status
  task.status = newStatus

  try {
    await tasksApi.updateTask(taskId, {
      status: newStatus,
      assignee_id: task.assignee_id,
      description: task.description,
      due_date: task.due_date,
    })
  } catch (e) {
    task.status = prevStatus
    ElMessage.error(getErrorMessage(e))
  }
}

function openTask(taskId: number) {
  router.push(`/projects/${id.value}/tasks/${taskId}`)
}

async function exportProject() {
  try {
    const blob = await projectsApi.exportProject(id.value)
    downloadBlob(blob, 'project.json')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  }
}

onMounted(load)
</script>

<template>
  <AppShell full-width>
    <div v-loading="loading">
      <PageHeader v-if="project" :title="project.title" :subtitle="project.description || undefined">
        <template #breadcrumbs>
          <router-link to="/projects">Проекты</router-link>
          <span> / {{ project.title }}</span>
        </template>
        <template #actions>
          <el-button type="primary" @click="router.push(`/projects/${id}/tasks/new`)">
            Новая задача
          </el-button>
          <el-button @click="exportProject">Экспорт</el-button>
          <el-button v-if="canEditProject" @click="router.push(`/projects/${id}/edit`)">
            Настройки
          </el-button>
          <el-button @click="router.push('/projects')">К проектам</el-button>
        </template>
      </PageHeader>

      <el-alert
        v-if="!loading && tasks.length === 0"
        type="info"
        :closable="false"
        show-icon
        class="tasks-hint"
        title="Задачи видны, если вы автор или исполнитель. Создайте задачу или попросите назначить вас исполнителем."
      />

      <TaskKanban
        v-if="!loading"
        :tasks="tasks"
        :users-map="usersMap"
        @drop-task="onDropTask"
        @open-task="openTask"
      />
    </div>
  </AppShell>
</template>

<style scoped>
.tasks-hint {
  margin-bottom: 1rem;
}
</style>
