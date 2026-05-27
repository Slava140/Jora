<script setup lang="ts">
import { computed } from 'vue'
import type { TaskWithMedia } from '@/types'
import { taskMediaCount } from '@/utils/media'

const props = defineProps<{
  task: TaskWithMedia
  assigneeName?: string
}>()

const attachmentCount = computed(() => taskMediaCount(props.task.media))

const emit = defineEmits<{
  click: []
}>()

function onDragStart(e: DragEvent) {
  const el = e.target as HTMLElement
  const taskId = el.dataset.taskId
  if (taskId && e.dataTransfer) {
    e.dataTransfer.setData('text/task-id', taskId)
    e.dataTransfer.effectAllowed = 'move'
  }
}
</script>

<template>
  <article
    class="task-card jora-card"
    draggable="true"
    :data-task-id="task.id"
    @dragstart="onDragStart"
    @click="emit('click')"
  >
    <div class="task-key">JORA-{{ task.id }}</div>
    <h4 class="task-title">{{ task.title }}</h4>
    <div class="task-meta">
      <span v-if="assigneeName" class="assignee">{{ assigneeName }}</span>
      <span v-if="attachmentCount" class="attachments" title="Вложения">
        📎 {{ attachmentCount }}
      </span>
    </div>
  </article>
</template>

<style scoped>
.task-card {
  padding: 0.75rem;
  cursor: grab;
  transition: box-shadow 0.15s;
}
.task-card:hover {
  box-shadow: 0 4px 8px rgba(9, 30, 66, 0.15);
}
.task-card:active {
  cursor: grabbing;
}
.task-key {
  font-size: 0.6875rem;
  color: var(--jora-text-muted);
  font-weight: 600;
  margin-bottom: 0.25rem;
}
.task-title {
  margin: 0 0 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  line-height: 1.35;
}
.task-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.75rem;
  color: var(--jora-text-muted);
}
.assignee {
  max-width: 70%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
