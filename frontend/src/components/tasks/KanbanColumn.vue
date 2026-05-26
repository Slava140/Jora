<script setup lang="ts">
import type { TaskStatus, TaskWithMedia } from '@/types'
import TaskCard from './TaskCard.vue'

const props = defineProps<{
  status: TaskStatus
  title: string
  tasks: TaskWithMedia[]
  usersMap: Record<number, string>
}>()

const emit = defineEmits<{
  dropTask: [taskId: number, status: TaskStatus]
  openTask: [taskId: number]
}>()

function onDragOver(e: DragEvent) {
  e.preventDefault()
  if (e.dataTransfer) e.dataTransfer.dropEffect = 'move'
}

function onDrop(e: DragEvent) {
  e.preventDefault()
  const taskId = e.dataTransfer?.getData('text/task-id')
  if (taskId) {
    emit('dropTask', parseInt(taskId, 10), props.status)
  }
}
</script>

<template>
  <section class="kanban-column" @dragover="onDragOver" @drop="onDrop">
    <header class="column-header">
      <h3>{{ title }}</h3>
      <span class="count">{{ tasks.length }}</span>
    </header>
    <div class="column-body">
      <TaskCard
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        :assignee-name="task.assignee_id ? usersMap[task.assignee_id] : undefined"
        @click="emit('openTask', task.id)"
      />
      <p v-if="tasks.length === 0" class="column-empty">Перетащите задачу сюда</p>
    </div>
  </section>
</template>

<style scoped>
.kanban-column {
  flex: 0 0 300px;
  min-width: 280px;
  background: #ebecf0;
  border-radius: var(--jora-radius);
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 220px);
}
.column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
}
.column-header h3 {
  margin: 0;
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: var(--jora-text-muted);
}
.count {
  font-size: 0.75rem;
  background: #dfe1e6;
  padding: 0.125rem 0.5rem;
  border-radius: 10px;
  font-weight: 600;
}
.column-body {
  flex: 1;
  overflow-y: auto;
  padding: 0 0.5rem 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.column-empty {
  text-align: center;
  font-size: 0.75rem;
  color: var(--jora-text-muted);
  padding: 1rem 0.5rem;
  margin: 0;
}
</style>
