<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
}>()
</script>

<template>
  <header class="page-header">
    <div class="page-header-text">
      <nav v-if="$slots.breadcrumbs" class="breadcrumbs">
        <slot name="breadcrumbs" />
      </nav>
      <h1>{{ title }}</h1>
      <p v-if="subtitle" class="subtitle">{{ subtitle }}</p>
    </div>
    <div v-if="$slots.actions" class="page-header-actions">
      <slot name="actions" />
    </div>
  </header>
</template>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}
.page-header h1 {
  margin: 0.25rem 0 0;
  font-size: 1.5rem;
  font-weight: 600;
}
.subtitle {
  margin: 0.5rem 0 0;
  color: var(--jora-text-muted);
  font-size: 0.875rem;
}
.breadcrumbs {
  font-size: 0.8125rem;
  color: var(--jora-text-muted);
  margin-bottom: 0.25rem;
}
.breadcrumbs :deep(a) {
  color: var(--jora-primary);
  text-decoration: none;
}
.breadcrumbs :deep(a:hover) {
  text-decoration: underline;
}
.page-header-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}
</style>
