<script setup lang="ts">
import { computed } from 'vue'
import type { TaskStatus, TaskWithMedia } from '@/types'
import KanbanColumn from './KanbanColumn.vue'

const props = defineProps<{
  tasks: TaskWithMedia[]
  usersMap: Record<number, string>
}>()

const emit = defineEmits<{
  dropTask: [taskId: number, status: TaskStatus]
  openTask: [taskId: number]
}>()

const columns: { status: TaskStatus; title: string }[] = [
  { status: 'open', title: 'Открыта' },
  { status: 'in_progress', title: 'В работе' },
  { status: 'finished', title: 'Завершена' },
]

const tasksByStatus = computed(() => {
  const map: Record<TaskStatus, TaskWithMedia[]> = {
    open: [],
    in_progress: [],
    finished: [],
  }
  for (const t of props.tasks) {
    map[t.status].push(t)
  }
  return map
})
</script>

<template>
  <div class="kanban-board">
    <KanbanColumn
      v-for="col in columns"
      :key="col.status"
      :status="col.status"
      :title="col.title"
      :tasks="tasksByStatus[col.status]"
      :users-map="usersMap"
      @drop-task="(id, status) => emit('dropTask', id, status)"
      @open-task="(id) => emit('openTask', id)"
    />
  </div>
</template>

<style scoped>
.kanban-board {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}
</style>
