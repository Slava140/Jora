<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import * as projectsApi from '@/api/projects'
import { getErrorMessage } from '@/utils/errors'

const visible = defineModel<boolean>('visible', { default: false })
const emit = defineEmits<{ imported: [] }>()

const loading = ref(false)

async function onUpload(file: File) {
  loading.value = true
  try {
    await projectsApi.importProject(file)
    ElMessage.success('Проект импортирован')
    visible.value = false
    emit('imported')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    loading.value = false
  }
  return false
}
</script>

<template>
  <el-dialog v-model="visible" title="Импорт проекта" width="480px">
    <p>Загрузите JSON-файл экспорта проекта.</p>
    <el-upload
      drag
      accept=".json,application/json"
      :auto-upload="true"
      :show-file-list="false"
      :before-upload="onUpload"
      :disabled="loading"
    >
      <div class="el-upload__text">Перетащите project.json</div>
    </el-upload>
  </el-dialog>
</template>
