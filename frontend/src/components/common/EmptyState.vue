<script setup lang="ts">
defineProps<{
  title?: string
  description?: string
}>()
</script>

<template>
  <div class="empty-state">
    <p v-if="title" class="empty-title">{{ title }}</p>
    <p v-if="description" class="empty-desc">{{ description }}</p>
    <slot />
  </div>
</template>

<style scoped>
.empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
  color: var(--jora-text-muted);
}
.empty-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--jora-text);
  margin: 0 0 0.5rem;
}
.empty-desc {
  margin: 0 0 1rem;
  font-size: 0.875rem;
}
</style>
