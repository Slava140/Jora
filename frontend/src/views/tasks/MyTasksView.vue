<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppShell from '@/components/layout/AppShell.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import TaskStatusBadge from '@/components/tasks/TaskStatusBadge.vue'
import PaginationBar from '@/components/PaginationBar.vue'
import TaskFilters from '@/components/TaskFilters.vue'
import * as tasksApi from '@/api/tasks'
import * as projectsApi from '@/api/projects'
import { formatDisplayDatetime } from '@/utils/datetime'
import { getErrorMessage } from '@/utils/errors'
import type { Project, TaskFilters as TFilters, TaskWithMedia } from '@/types'

const router = useRouter()

const tasks = ref<TaskWithMedia[]>([])
const projects = ref<Project[]>([])
const loading = ref(false)
const page = ref(1)
const limit = ref(12)

const filters = ref<TFilters>({ page: 1, limit: 12 })

const projectsMap = computed(() =>
  Object.fromEntries(projects.value.map((p) => [p.id, p.title])),
)

async function loadRefs() {
  projects.value = await projectsApi.getProjects({ page: 1, limit: 100 })
}

function applyFilters() {
  page.value = 1
  load()
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

function openTask(task: TaskWithMedia) {
  router.push(`/projects/${task.project_id}/tasks/${task.id}`)
}

onMounted(async () => {
  await loadRefs()
  await load()
})
</script>

<template>
  <AppShell>
    <PageHeader title="Мои задачи" subtitle="Все задачи, где вы автор или исполнитель" />

    <TaskFilters v-model="filters" :projects="projects" :users="[]" @apply="applyFilters" />

    <div v-loading="loading" class="task-cards">
      <article
        v-for="task in tasks"
        :key="task.id"
        class="my-task-card jora-card"
        @click="openTask(task)"
      >
        <div class="card-top">
          <span class="task-key">JORA-{{ task.id }}</span>
          <TaskStatusBadge :status="task.status" />
        </div>
        <h3>{{ task.title }}</h3>
        <p class="project-name">{{ projectsMap[task.project_id] ?? `Проект #${task.project_id}` }}</p>
        <footer>
          <span>Срок: {{ formatDisplayDatetime(task.due_date) }}</span>
        </footer>
      </article>
    </div>

    <EmptyState
      v-if="!loading && tasks.length === 0"
      title="Нет задач"
      description="Создайте задачу в проекте или измените фильтры."
    />

    <PaginationBar
      v-model:page="page"
      v-model:limit="limit"
      :item-count="tasks.length"
      @change="load"
    />
  </AppShell>
</template>

<style scoped>
.task-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}
.my-task-card {
  padding: 1rem 1.25rem;
  cursor: pointer;
  transition: box-shadow 0.15s;
}
.my-task-card:hover {
  box-shadow: 0 4px 12px rgba(9, 30, 66, 0.12);
}
.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.task-key {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--jora-text-muted);
}
.my-task-card h3 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
}
.project-name {
  margin: 0 0 0.75rem;
  font-size: 0.875rem;
  color: var(--jora-primary);
}
footer {
  font-size: 0.75rem;
  color: var(--jora-text-muted);
}
</style>
