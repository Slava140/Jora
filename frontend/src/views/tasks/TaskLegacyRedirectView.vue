<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as tasksApi from '@/api/tasks'
import { getErrorMessage } from '@/utils/errors'

const props = defineProps<{ id: string }>()
const router = useRouter()

onMounted(async () => {
  const taskId = parseInt(props.id, 10)
  try {
    const task = await tasksApi.getTaskById(taskId)
    await router.replace(`/projects/${task.project_id}/tasks/${task.id}`)
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
    router.replace('/my-tasks')
  }
})
</script>

<template>
  <div class="redirect-loading">Перенаправление…</div>
</template>

<style scoped>
.redirect-loading {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--jora-text-muted);
}
</style>
