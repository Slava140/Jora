<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import * as mediaApi from '@/api/media'
import { getErrorMessage } from '@/utils/errors'

const props = defineProps<{ taskId: number }>()
const emit = defineEmits<{ uploaded: [] }>()

const uploading = ref(false)

async function onUpload(file: File) {
  uploading.value = true
  try {
    await mediaApi.uploadMedia(file, props.taskId)
    ElMessage.success('Файл загружен')
    emit('uploaded')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    uploading.value = false
  }
  return false
}
</script>

<template>
  <div class="media-upload">
    <el-upload
      :auto-upload="true"
      :show-file-list="false"
      :before-upload="onUpload"
      :disabled="uploading"
      drag
    >
      <div class="el-upload__text">Перетащите файл или <em>нажмите</em></div>
    </el-upload>
  </div>
</template>

<style scoped>
.media-upload {
  margin-bottom: 1rem;
}
</style>
