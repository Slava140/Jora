<script setup lang="ts">
import { reactive, ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import AppShell from '@/components/layout/AppShell.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import * as projectsApi from '@/api/projects'
import { useAuthStore } from '@/stores/auth'
import { getErrorMessage } from '@/utils/errors'

const props = defineProps<{ projectId?: string }>()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const projectId = computed(() => {
  const raw = props.projectId ?? route.params.projectId
  return raw ? parseInt(String(raw), 10) : null
})
const isEdit = computed(() => projectId.value != null)

const form = reactive({ title: '', description: '' })
const loading = ref(false)
const saving = ref(false)

async function load() {
  if (!projectId.value) return
  loading.value = true
  try {
    const p = await projectsApi.getProjectById(projectId.value)
    if (p.owner_id !== auth.user?.id) {
      ElMessage.error('Нет прав на редактирование проекта')
      router.push(`/projects/${projectId.value}`)
      return
    }
    form.title = p.title
    form.description = p.description ?? ''
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
    router.push('/projects')
  } finally {
    loading.value = false
  }
}

async function save() {
  saving.value = true
  try {
    const body = { title: form.title, description: form.description || null }
    if (isEdit.value && projectId.value) {
      await projectsApi.updateProject(projectId.value, body)
      ElMessage.success('Проект обновлён')
      router.push(`/projects/${projectId.value}`)
    } else {
      const created = await projectsApi.createProject(body)
      ElMessage.success('Проект создан')
      router.push(`/projects/${created.id}`)
    }
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    saving.value = false
  }
}

async function remove() {
  if (!projectId.value) return
  await ElMessageBox.confirm('Удалить проект?', 'Подтверждение', { type: 'warning' })
  try {
    await projectsApi.deleteProject(projectId.value)
    ElMessage.success('Проект удалён')
    router.push('/projects')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  }
}

onMounted(load)
</script>

<template>
  <AppShell>
    <PageHeader :title="isEdit ? 'Настройки проекта' : 'Новый проект'">
      <template #breadcrumbs>
        <router-link to="/projects">Проекты</router-link>
        <span v-if="isEdit"> / Настройки</span>
      </template>
      <template #actions>
        <el-button @click="router.back()">Отмена</el-button>
      </template>
    </PageHeader>

    <el-card v-loading="loading" class="form-card">
      <el-form label-position="top" @submit.prevent="save">
        <el-form-item label="Название" required>
          <el-input v-model="form.title" minlength="3" maxlength="255" />
        </el-form-item>
        <el-form-item label="Описание">
          <el-input v-model="form.description" type="textarea" maxlength="500" :rows="4" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="saving">Сохранить</el-button>
          <el-button v-if="isEdit" type="danger" @click="remove">Удалить проект</el-button>
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
