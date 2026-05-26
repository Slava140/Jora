<script setup lang="ts">
import type { Project } from '@/types'
import ProjectCard from './ProjectCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'

defineProps<{
  projects: Project[]
  loading?: boolean
  currentUserId?: number
}>()

const emit = defineEmits<{ open: [id: number] }>()
</script>

<template>
  <div v-loading="loading" class="project-grid-wrap">
    <div v-if="!loading && projects.length" class="project-grid">
      <ProjectCard
        v-for="p in projects"
        :key="p.id"
        :project="p"
        :is-owner="currentUserId === p.owner_id"
        @click="emit('open', p.id)"
      />
    </div>
    <EmptyState
      v-else-if="!loading"
      title="Нет проектов"
      description="Создайте первый проект или дождитесь приглашения в существующий."
    >
      <slot name="empty-action" />
    </EmptyState>
  </div>
</template>

<style scoped>
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}
</style>
