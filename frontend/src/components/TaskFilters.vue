<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Project, TaskFilters, TaskStatus, User } from '@/types'

const model = defineModel<TaskFilters>({ required: true })

defineProps<{
  projects: Project[]
  users: User[]
}>()

const emit = defineEmits<{ apply: [] }>()

const localFrom = ref(model.value.from ?? '')
const localTo = ref(model.value.to ?? '')

watch([localFrom, localTo], () => {
  if (localFrom.value && localTo.value) {
    model.value.from = localFrom.value
    model.value.to = localTo.value
  } else if (!localFrom.value && !localTo.value) {
    model.value.from = undefined
    model.value.to = undefined
  }
})

const statuses: { label: string; value: TaskStatus | '' }[] = [
  { label: 'Все', value: '' },
  { label: 'Открыта', value: 'open' },
  { label: 'В работе', value: 'in_progress' },
  { label: 'Завершена', value: 'finished' },
]
</script>

<template>
  <el-card shadow="never" class="filters">
    <el-form :inline="true" @submit.prevent="emit('apply')">
      <el-form-item label="Проект">
        <el-select v-model="model.project_id" clearable placeholder="Все" style="width: 160px">
          <el-option
            v-for="p in projects"
            :key="p.id"
            :label="p.title"
            :value="p.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="Статус">
        <el-select v-model="model.status" clearable placeholder="Все" style="width: 140px">
          <el-option
            v-for="s in statuses"
            :key="s.value"
            :label="s.label"
            :value="s.value || undefined"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="Название">
        <el-input v-model="model.title" clearable placeholder="Поиск" style="width: 160px" />
      </el-form-item>
      <el-form-item label="Автор">
        <el-select v-model="model.author_id" clearable placeholder="Все" style="width: 160px">
          <el-option v-for="u in users" :key="u.id" :label="u.username" :value="u.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="Исполнитель">
        <el-select v-model="model.assignee_id" clearable placeholder="Все" style="width: 160px">
          <el-option v-for="u in users" :key="u.id" :label="u.username" :value="u.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="С">
        <el-date-picker v-model="localFrom" type="date" value-format="YYYY-MM-DD" clearable />
      </el-form-item>
      <el-form-item label="По">
        <el-date-picker v-model="localTo" type="date" value-format="YYYY-MM-DD" clearable />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit">Применить</el-button>
        <el-button
          @click="
            model.project_id = undefined;
            model.status = undefined;
            model.title = undefined;
            model.author_id = undefined;
            model.assignee_id = undefined;
            localFrom = '';
            localTo = '';
            model.from = undefined;
            model.to = undefined;
            emit('apply')
          "
        >
          Сбросить
        </el-button>
      </el-form-item>
    </el-form>
    <el-alert
      v-if="(localFrom && !localTo) || (!localFrom && localTo)"
      type="warning"
      :closable="false"
      title="Укажите обе даты «С» и «По» или оставьте обе пустыми"
      show-icon
      class="date-warn"
    />
  </el-card>
</template>

<style scoped>
.filters {
  margin-bottom: 1rem;
}
.date-warn {
  margin-top: 0.5rem;
}
</style>
