<script setup lang="ts">
import { reactive, ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppShell from '@/components/layout/AppShell.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import * as tasksApi from '@/api/tasks'
import * as projectsApi from '@/api/projects'
import { fromDateInputValue } from '@/utils/datetime'
import { getErrorMessage } from '@/utils/errors'
import type { Project, TaskStatus } from '@/types'

const props = defineProps<{ projectId: string }>()
const router = useRouter()

const projectIdNum = computed(() => parseInt(props.projectId, 10))
const project = ref<Project | null>(null)
const saving = ref(false)

const form = reactive({
  title: '',
  description: '',
  status: 'open' as TaskStatus,
  due_date_local: '',
})

async function load() {
  try {
    project.value = await projectsApi.getProjectById(projectIdNum.value)
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
    router.push('/projects')
  }
}

async function save() {
  saving.value = true
  try {
    const created = await tasksApi.createTask({
      title: form.title,
      description: form.description,
      status: form.status,
      project_id: projectIdNum.value,
      due_date: fromDateInputValue(form.due_date_local),
    })
    ElMessage.success('Задача создана')
    router.push(`/projects/${projectIdNum.value}/tasks/${created.id}`)
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<template>
  <AppShell>
    <PageHeader v-if="project" title="Новая задача">
      <template #breadcrumbs>
        <router-link to="/projects">Проекты</router-link>
        <span> / </span>
        <router-link :to="`/projects/${projectIdNum}`">{{ project.title }}</router-link>
        <span> / Создание</span>
      </template>
      <template #actions>
        <el-button @click="router.push(`/projects/${projectIdNum}`)">Отмена</el-button>
      </template>
    </PageHeader>

    <el-card class="form-card">
      <el-form label-position="top" @submit.prevent="save">
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
        </el-form-item>
      </el-form>
    </el-card>
  </AppShell>
</template>

<style scoped>
.form-card {
  max-width: 640px;
}
</style>
