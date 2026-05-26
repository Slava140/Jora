<script setup lang="ts">
import { computed } from 'vue'

const page = defineModel<number>('page', { default: 1 })
const limit = defineModel<number>('limit', { default: 10 })

const props = withDefaults(
  defineProps<{
    itemCount?: number
  }>(),
  { itemCount: 0 },
)

const emit = defineEmits<{ change: [] }>()

const hasNext = computed(() => props.itemCount >= limit.value)
const hasPrev = computed(() => page.value > 1)
const visible = computed(() => hasNext.value || hasPrev.value)

function goPrev() {
  if (!hasPrev.value) return
  page.value -= 1
  emit('change')
}

function goNext() {
  if (!hasNext.value) return
  page.value += 1
  emit('change')
}

function onLimitChange() {
  page.value = 1
  emit('change')
}
</script>

<template>
  <div v-if="visible" class="pagination-bar">
    <el-button :disabled="!hasPrev" @click="goPrev">Назад</el-button>
    <span class="page-label">Страница {{ page }}</span>
    <el-button :disabled="!hasNext" @click="goNext">Вперёд</el-button>
    <el-select v-model="limit" class="limit-select" @change="onLimitChange">
      <el-option v-for="n in [5, 10, 12, 20, 50]" :key="n" :label="`${n} на странице`" :value="n" />
    </el-select>
  </div>
</template>

<style scoped>
.pagination-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}
.page-label {
  font-size: 0.875rem;
  color: var(--jora-text-muted);
  min-width: 6rem;
  text-align: center;
}
.limit-select {
  width: 160px;
  margin-left: auto;
}
</style>
