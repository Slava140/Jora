<script setup lang="ts">
import type { Project } from '@/types'
import { formatDisplayDatetime } from '@/utils/datetime'

defineProps<{
  project: Project
  isOwner?: boolean
}>()

const emit = defineEmits<{ click: [] }>()
</script>

<template>
  <article class="project-card jora-card" @click="emit('click')">
    <div class="card-top">
      <h3>{{ project.title }}</h3>
      <el-tag v-if="isOwner" size="small" type="info">Владелец</el-tag>
    </div>
    <p class="description">
      {{ project.description || 'Без описания' }}
    </p>
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
.card-footer {
  margin-top: 1rem;
  font-size: 0.75rem;
  color: var(--jora-text-muted);
}
</style>
