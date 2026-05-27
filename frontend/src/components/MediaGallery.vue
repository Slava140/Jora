<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { fetchAuthenticatedBlob } from '@/utils/blob'
import { uniqueTaskMedia } from '@/utils/media'
import { getErrorMessage } from '@/utils/errors'
import type { TaskMedia } from '@/types'

const props = defineProps<{
  media: TaskMedia[]
}>()

const items = ref<{ id: number; url: string; filename: string; previewUrl: string }[]>([])
const loading = ref(false)

const mediaItems = computed(() => uniqueTaskMedia(props.media))

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
    for (const m of mediaItems.value) {
      const blob = await fetchAuthenticatedBlob(m.id, true)
      const previewUrl = URL.createObjectURL(blob)
      blobUrls.push(previewUrl)
      items.value.push({
        id: m.id,
        url: m.url,
        filename: m.filename,
        previewUrl,
      })
    }
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    loading.value = false
  }
}

async function downloadItem(item: { id: number; filename: string }) {
  try {
    const blob = await fetchAuthenticatedBlob(item.id, true)
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = item.filename
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  }
}

function isImageFilename(filename: string): boolean {
  return /\.(jpg|jpeg|png|gif|bmp|webp)$/i.test(filename)
}

watch(() => props.media, load, { deep: true })
onMounted(load)
onUnmounted(revokeAll)

defineExpose({ reload: load })
</script>

<template>
  <div class="gallery">
    <h3 class="gallery-title">Файлы</h3>
    <el-skeleton v-if="loading" :rows="2" animated />
    <el-empty v-else-if="items.length === 0" description="Нет вложений" />
    <ul v-else class="file-list">
      <li v-for="item in items" :key="item.id" class="file-item">
        <div class="file-preview">
          <img
            v-if="isImageFilename(item.filename)"
            :src="item.previewUrl"
            :alt="item.filename"
            class="preview-img"
          />
          <div v-else class="file-icon" aria-hidden="true">📄</div>
        </div>
        <div class="file-info">
          <span class="file-name" :title="item.filename">{{ item.filename }}</span>
          <el-button size="small" @click="downloadItem(item)">Скачать</el-button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.gallery-title {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 600;
}
.file-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.file-item {
  display: flex;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem;
  background: var(--jora-bg);
  border: 1px solid var(--jora-border);
  border-radius: var(--jora-radius);
}
.file-preview {
  flex-shrink: 0;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--jora-surface);
  border-radius: 4px;
  overflow: hidden;
}
.preview-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.file-icon {
  font-size: 1.75rem;
}
.file-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}
.file-name {
  font-size: 0.875rem;
  font-weight: 500;
  word-break: break-all;
  color: var(--jora-text);
}
</style>
