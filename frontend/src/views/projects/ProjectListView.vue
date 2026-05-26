<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppShell from '@/components/layout/AppShell.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import ProjectGrid from '@/components/projects/ProjectGrid.vue'
import PaginationBar from '@/components/PaginationBar.vue'
import ImportProjectDialog from '@/components/ImportProjectDialog.vue'
import * as projectsApi from '@/api/projects'
import { useAuthStore } from '@/stores/auth'
import { getErrorMessage } from '@/utils/errors'
import type { Project } from '@/types'

const router = useRouter()
const auth = useAuthStore()

const projects = ref<Project[]>([])
const loading = ref(false)
const page = ref(1)
const limit = ref(12)
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

function openProject(id: number) {
  router.push(`/projects/${id}`)
}

onMounted(load)
</script>

<template>
  <AppShell>
    <PageHeader title="Ваши проекты" subtitle="Выберите проект, чтобы открыть доску задач">
      <template #actions>
        <el-button type="primary" @click="router.push('/projects/new')">Создать проект</el-button>
        <el-button @click="importVisible = true">Импорт</el-button>
      </template>
    </PageHeader>

    <ProjectGrid
      :projects="projects"
      :loading="loading"
      :current-user-id="auth.user?.id"
      @open="openProject"
    >
      <template #empty-action>
        <el-button type="primary" @click="router.push('/projects/new')">Создать проект</el-button>
      </template>
    </ProjectGrid>

    <PaginationBar
      v-model:page="page"
      v-model:limit="limit"
      :item-count="projects.length"
      @change="load"
    />
    <ImportProjectDialog v-model:visible="importVisible" @imported="load" />
  </AppShell>
</template>
