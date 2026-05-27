<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Project, TaskWithMedia } from '@/types'
import TaskStatusBadge from '@/components/tasks/TaskStatusBadge.vue'
import { formatDisplayDatetime } from '@/utils/datetime'

const props = defineProps<{
  project: Project
  isOwner?: boolean
  previewTasks?: TaskWithMedia[]
}>()

const emit = defineEmits<{ click: [] }>()
const router = useRouter()

function openProject() {
  emit('click')
}

function openTask(task: TaskWithMedia, e: Event) {
  e.stopPropagation()
  router.push(`/projects/${props.project.id}/tasks/${task.id}`)
}
</script>

<template>
  <article class="project-card jora-card" @click="openProject">
    <div class="card-top">
      <h3>{{ project.title }}</h3>
      <el-tag v-if="isOwner" size="small" type="info">Владелец</el-tag>
    </div>
    <p class="description">
      {{ project.description || 'Без описания' }}
    </p>

    <div v-if="previewTasks?.length" class="preview-tasks">
      <p class="preview-label">Задачи</p>
      <ul class="task-preview-list">
        <li
          v-for="task in previewTasks"
          :key="task.id"
          class="task-preview-item"
          @click="openTask(task, $event)"
        >
          <span class="task-preview-key">JORA-{{ task.id }}</span>
          <span class="task-preview-title">{{ task.title }}</span>
          <TaskStatusBadge :status="task.status" />
        </li>
      </ul>
    </div>

    <footer class="card-footer">
      <span>Обновлён {{ formatDisplayDatetime(project.updated_at) }}</span>
    </footer>
  </article>
</template>

<style scoped>
.project-card {
  padding: 1rem 1.25rem;
  cursor: pointer;
  transition: box-shadow 0.15s, border-color 0.15s;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.project-card:hover {
  border-color: var(--jora-primary);
  box-shadow: 0 4px 12px rgba(9, 30, 66, 0.12);
}
.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.project-card h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.3;
}
.description {
  flex: 1;
  margin: 0;
  font-size: 0.875rem;
  color: var(--jora-text-muted);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.preview-tasks {
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--jora-border);
}
.preview-label {
  margin: 0 0 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--jora-text-muted);
}
.task-preview-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}
.task-preview-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.5rem;
  border-radius: 4px;
  font-size: 0.8125rem;
  cursor: pointer;
}
.task-preview-item:hover {
  background: var(--jora-bg);
}
.task-preview-key {
  flex-shrink: 0;
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--jora-text-muted);
}
.task-preview-title {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--jora-text);
}
.card-footer {
  margin-top: 1rem;
  font-size: 0.75rem;
  color: var(--jora-text-muted);
}
</style>
