<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { extractMediaId, fetchAuthenticatedBlob } from '@/utils/blob'
import { getErrorMessage } from '@/utils/errors'

const props = defineProps<{
  mediaUrls: string[]
}>()

const items = ref<{ id: number; url: string; filename: string }[]>([])
const useOriginal = ref(false)
const loading = ref(false)

const blobUrls: string[] = []

function revokeAll() {
  blobUrls.forEach((u) => URL.revokeObjectURL(u))
  blobUrls.length = 0
}

async function load() {
  revokeAll()
  items.value = []
  loading.value = true
  try {
    for (const mediaUrl of props.mediaUrls) {
      const id = extractMediaId(mediaUrl)
      if (id == null) continue
      const blob = await fetchAuthenticatedBlob(id, useOriginal.value)
      const url = URL.createObjectURL(blob)
      blobUrls.push(url)
      const filename = mediaUrl.split('/').pop()?.split('?')[0] ?? `media-${id}`
      items.value.push({ id, url, filename })
    }
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    loading.value = false
  }
}

async function downloadItem(id: number) {
  try {
    const blob = await fetchAuthenticatedBlob(id, useOriginal.value)
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `media-${id}`
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  }
}

watch(() => [props.mediaUrls, useOriginal.value], load, { deep: true })
onMounted(load)
onUnmounted(revokeAll)

defineExpose({ reload: load })
</script>

<template>
  <div class="gallery">
    <div class="gallery-header">
      <h3>Медиа</h3>
      <el-switch
        v-model="useOriginal"
        active-text="Оригинал"
        inactive-text="Сжатый"
      />
    </div>
    <el-skeleton v-if="loading" :rows="2" animated />
    <el-empty v-else-if="items.length === 0" description="Нет вложений" />
    <div v-else class="grid">
      <div v-for="item in items" :key="item.id" class="grid-item">
        <img
          v-if="item.url.startsWith('blob:') && /\.(jpg|jpeg|png|gif|bmp)/i.test(item.filename)"
          :src="item.url"
          :alt="item.filename"
          class="preview"
        />
        <div v-else class="file-placeholder">{{ item.filename }}</div>
        <el-button size="small" @click="downloadItem(item.id)">Скачать</el-button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gallery-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}
.gallery-header h3 {
  margin: 0;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
}
.grid-item {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.5rem;
  text-align: center;
}
.preview {
  max-width: 100%;
  max-height: 120px;
  object-fit: contain;
  margin-bottom: 0.5rem;
}
.file-placeholder {
  padding: 2rem 0.5rem;
  font-size: 0.8rem;
  color: #64748b;
  word-break: break-all;
}
</style>
