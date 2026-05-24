<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppLayout from '@/components/AppLayout.vue'
import * as tasksApi from '@/api/tasks'
import * as projectsApi from '@/api/projects'
import { fromDateInputValue } from '@/utils/datetime'
import { getErrorMessage } from '@/utils/errors'
import type { Project, TaskStatus } from '@/types'

const route = useRoute()
const router = useRouter()

const projects = ref<Project[]>([])
const saving = ref(false)

const form = reactive({
  title: '',
  description: '',
  status: 'open' as TaskStatus,
  project_id: null as number | null,
  due_date_local: '',
})

async function load() {
  projects.value = await projectsApi.getProjects({ page: 1, limit: 100 })
  const qProject = route.query.project_id
  if (qProject) {
    form.project_id = parseInt(String(qProject), 10)
  } else if (projects.value.length) {
    form.project_id = projects.value[0].id
  }
}

async function save() {
  if (!form.project_id) {
    ElMessage.warning('Выберите проект')
    return
  }
  saving.value = true
  try {
    const created = await tasksApi.createTask({
      title: form.title,
      description: form.description,
      status: form.status,
      project_id: form.project_id,
      due_date: fromDateInputValue(form.due_date_local),
    })
    ElMessage.success('Задача создана')
    router.push(`/tasks/${created.id}`)
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <el-card>
      <h1>Новая задача</h1>
      <el-form label-position="top" @submit.prevent="save">
        <el-form-item label="Проект" required>
          <el-select v-model="form.project_id" placeholder="Проект" style="width: 100%">
            <el-option v-for="p in projects" :key="p.id" :label="p.title" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="Название" required>
          <el-input v-model="form.title" minlength="3" maxlength="255" />
        </el-form-item>
        <el-form-item label="Описание">
          <el-input v-model="form.description" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="Статус">
          <el-select v-model="form.status">
            <el-option label="Открыта" value="open" />
            <el-option label="В работе" value="in_progress" />
            <el-option label="Завершена" value="finished" />
          </el-select>
        </el-form-item>
        <el-form-item label="Срок">
          <el-date-picker
            v-model="form.due_date_local"
            type="datetime"
            value-format="YYYY-MM-DDTHH:mm"
            placeholder="Не указан"
            clearable
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="saving">Создать</el-button>
          <el-button @click="router.back()">Отмена</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </AppLayout>
</template>

<style scoped>
h1 {
  margin: 0 0 1rem;
}
</style>
