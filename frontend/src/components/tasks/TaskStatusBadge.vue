<script setup lang="ts">
import type { TaskStatus } from '@/types'

const props = defineProps<{ status: TaskStatus }>()

const labels: Record<TaskStatus, string> = {
  open: 'Открыта',
  in_progress: 'В работе',
  finished: 'Завершена',
}
</script>

<template>
  <span class="badge" :class="`badge--${props.status}`">{{ labels[props.status] }}</span>
</template>

<style scoped>
.badge {
  display: inline-block;
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}
.badge--open {
  background: var(--jora-status-open);
  color: var(--jora-text);
}
.badge--in_progress {
  background: var(--jora-status-progress);
  color: #0747a6;
}
.badge--finished {
  background: var(--jora-status-finished);
  color: #006644;
}
</style>
