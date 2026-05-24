<script setup lang="ts">
const page = defineModel<number>('page', { default: 1 })
const limit = defineModel<number>('limit', { default: 10 })
const emit = defineEmits<{ change: [] }>()
</script>

<template>
  <div class="pagination-bar">
    <el-pagination
      v-model:current-page="page"
      v-model:page-size="limit"
      :page-sizes="[5, 10, 20, 50]"
      layout="sizes, prev, pager, next"
      :total="10000"
      background
      @current-change="emit('change')"
      @size-change="emit('change')"
    />
    <span class="hint">Пагинация без total от API — листайте, пока список не пуст</span>
  </div>
</template>

<style scoped>
.pagination-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}
.hint {
  font-size: 0.75rem;
  color: #64748b;
}
</style>
