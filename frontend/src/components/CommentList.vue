<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import * as commentsApi from '@/api/comments'
import { formatDisplayDatetime } from '@/utils/datetime'
import { getErrorMessage } from '@/utils/errors'
import type { Comment } from '@/types'

const props = defineProps<{
  taskId: number
  usersMap: Record<number, string>
}>()

const comments = ref<Comment[]>([])
const loading = ref(false)
const newContent = ref('')
const submitting = ref(false)

async function load() {
  loading.value = true
  try {
    comments.value = await commentsApi.getComments({
      task_id: props.taskId,
      page: 1,
      limit: 100,
    })
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    loading.value = false
  }
}

async function submit() {
  if (!newContent.value.trim()) return
  submitting.value = true
  try {
    await commentsApi.createComment({
      content: newContent.value.trim(),
      task_id: props.taskId,
    })
    newContent.value = ''
    await load()
    ElMessage.success('Комментарий добавлен')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    submitting.value = false
  }
}

onMounted(load)

defineExpose({ reload: load })
</script>

<template>
  <div class="comments">
    <h3>Комментарии</h3>
    <el-skeleton v-if="loading" :rows="3" animated />
    <el-empty v-else-if="comments.length === 0" description="Нет комментариев" />
    <div v-else class="comment-list">
      <div v-for="c in comments" :key="c.id" class="comment-item">
        <div class="comment-meta">
          <strong>{{ usersMap[c.author_id] ?? `User #${c.author_id}` }}</strong>
          <span>{{ formatDisplayDatetime(c.created_at) }}</span>
        </div>
        <p>{{ c.content }}</p>
      </div>
    </div>
    <el-input
      v-model="newContent"
      type="textarea"
      :rows="3"
      placeholder="Новый комментарий"
      class="comment-input"
    />
    <el-button type="primary" :loading="submitting" @click="submit">Отправить</el-button>
  </div>
</template>

<style scoped>
.comments h3 {
  margin: 0 0 1rem;
}
.comment-item {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
}
.comment-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}
.comment-input {
  margin: 1rem 0 0.5rem;
}
</style>
