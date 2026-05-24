<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppLayout from '@/components/AppLayout.vue'
import PaginationBar from '@/components/PaginationBar.vue'
import ImportProjectDialog from '@/components/ImportProjectDialog.vue'
import * as projectsApi from '@/api/projects'
import { useAuthStore } from '@/stores/auth'
import { formatDisplayDatetime } from '@/utils/datetime'
import { getErrorMessage } from '@/utils/errors'
import type { Project } from '@/types'

const router = useRouter()
const auth = useAuthStore()

const projects = ref<Project[]>([])
const loading = ref(false)
const page = ref(1)
const limit = ref(10)
const importVisible = ref(false)

async function load() {
  loading.value = true
  try {
    projects.value = await projectsApi.getProjects({ page: page.value, limit: limit.value })
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="page-header">
      <h1>Проекты</h1>
      <div class="actions">
        <template v-if="auth.isAuthenticated">
          <el-button type="primary" @click="router.push('/projects/new')">Создать</el-button>
          <el-button @click="importVisible = true">Импорт</el-button>
        </template>
      </div>
    </div>

    <el-table v-loading="loading" :data="projects" stripe @row-click="(row: Project) => router.push(`/projects/${row.id}`)">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="title" label="Название" />
      <el-table-column prop="description" label="Описание" show-overflow-tooltip />
      <el-table-column label="Создан">
        <template #default="{ row }">{{ formatDisplayDatetime(row.created_at) }}</template>
      </el-table-column>
      <el-table-column label="" width="100">
        <template #default="{ row }">
          <el-button text type="primary" @click.stop="router.push(`/projects/${row.id}`)">
            Открыть
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <PaginationBar v-model:page="page" v-model:limit="limit" @change="load" />
    <ImportProjectDialog v-model:visible="importVisible" @imported="load" />
  </AppLayout>
</template>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.page-header h1 {
  margin: 0;
}
.actions {
  display: flex;
  gap: 0.5rem;
}
:deep(.el-table__row) {
  cursor: pointer;
}
</style>
