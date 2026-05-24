<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import AppLayout from '@/components/AppLayout.vue'
import CommentList from '@/components/CommentList.vue'
import MediaGallery from '@/components/MediaGallery.vue'
import MediaUpload from '@/components/MediaUpload.vue'
import * as tasksApi from '@/api/tasks'
import * as usersApi from '@/api/users'
import { useAuthStore } from '@/stores/auth'
import { formatDisplayDatetime } from '@/utils/datetime'
import { getErrorMessage } from '@/utils/errors'
import type { TaskStatus, TaskWithMedia, User } from '@/types'

const props = defineProps<{ id: string }>()
const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const taskId = computed(() => parseInt(props.id, 10))
const task = ref<TaskWithMedia | null>(null)
const users = ref<User[]>([])
const loading = ref(false)
const saving = ref(false)

const editStatus = ref<TaskStatus>('open')
const editAssignee = ref<number | null>(null)

const usersMap = computed(() =>
  Object.fromEntries(users.value.map((u) => [u.id, u.username])),
)

const statusLabels: Record<string, string> = {
  open: 'Открыта',
  in_progress: 'В работе',
  finished: 'Завершена',
}

const galleryRef = ref<InstanceType<typeof MediaGallery> | null>(null)

const canDelete = computed(() => {
  if (!task.value || !auth.user) return false
  return task.value.author_id === auth.user.id
})

async function load() {
  loading.value = true
  try {
    const [t, u] = await Promise.all([
      tasksApi.getTaskById(taskId.value),
      usersApi.getUsers({ page: 1, limit: 100 }),
    ])
    task.value = t
    users.value = u
    editStatus.value = t.status
    editAssignee.value = t.assignee_id
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
    router.push('/tasks')
  } finally {
    loading.value = false
  }
}

async function saveUpdate() {
  if (!task.value) return
  saving.value = true
  try {
    const updated = await tasksApi.updateTask(taskId.value, {
      status: editStatus.value,
      assignee_id: editAssignee.value,
    })
    task.value = { ...task.value, ...updated, media: task.value.media }
    ElMessage.success('Задача обновлена')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    saving.value = false
  }
}

async function remove() {
  await ElMessageBox.confirm('Удалить задачу?', 'Подтверждение', { type: 'warning' })
  try {
    await tasksApi.deleteTask(taskId.value)
    ElMessage.success('Задача удалена')
    router.push('/tasks')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  }
}

function onMediaUploaded() {
  load()
  galleryRef.value?.reload()
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div v-loading="loading">
      <template v-if="task">
        <div class="page-header">
          <div>
            <h1>{{ task.title }}</h1>
            <el-tag>{{ statusLabels[task.status] ?? task.status }}</el-tag>
          </div>
          <el-button @click="router.back()">Назад</el-button>
        </div>

        <el-card class="section">
          <p>{{ task.description }}</p>
          <dl class="meta-grid">
            <dt>Проект</dt>
            <dd>
              <router-link :to="`/projects/${task.project_id}`">#{{ task.project_id }}</router-link>
            </dd>
            <dt>Автор</dt>
            <dd>{{ usersMap[task.author_id] ?? task.author_id }}</dd>
            <dt>Исполнитель</dt>
            <dd>{{ task.assignee_id ? usersMap[task.assignee_id] ?? task.assignee_id : '—' }}</dd>
            <dt>Срок</dt>
            <dd>{{ formatDisplayDatetime(task.due_date) }}</dd>
            <dt>Создана</dt>
            <dd>{{ formatDisplayDatetime(task.created_at) }}</dd>
            <dt>Обновлена</dt>
            <dd>{{ formatDisplayDatetime(task.updated_at) }}</dd>
          </dl>
        </el-card>

        <el-card class="section">
          <h3>Обновить статус и исполнителя</h3>
          <el-form :inline="true" @submit.prevent="saveUpdate">
            <el-form-item label="Статус">
              <el-select v-model="editStatus">
                <el-option label="Открыта" value="open" />
                <el-option label="В работе" value="in_progress" />
                <el-option label="Завершена" value="finished" />
              </el-select>
            </el-form-item>
            <el-form-item label="Исполнитель">
              <el-select v-model="editAssignee" clearable placeholder="Не назначен">
                <el-option
                  v-for="u in users"
                  :key="u.id"
                  :label="u.username"
                  :value="u.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" native-type="submit" :loading="saving">Сохранить</el-button>
            </el-form-item>
          </el-form>
          <p class="hint">Редактировать могут автор, исполнитель или администратор (по правилам API).</p>
          <el-button v-if="canDelete" type="danger" @click="remove">Удалить задачу</el-button>
        </el-card>

        <el-card class="section">
          <MediaUpload :task-id="taskId" @uploaded="onMediaUploaded" />
          <MediaGallery ref="galleryRef" :media-urls="task.media ?? []" />
        </el-card>

        <el-card class="section">
          <CommentList :task-id="taskId" :users-map="usersMap" />
        </el-card>
      </template>
    </div>
  </AppLayout>
</template>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}
.page-header h1 {
  margin: 0 0.5rem 0 0;
}
.section {
  margin-bottom: 1rem;
}
.meta-grid {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 0.5rem 1rem;
  margin: 1rem 0 0;
}
.meta-grid dt {
  color: #64748b;
  font-size: 0.875rem;
}
.meta-grid dd {
  margin: 0;
}
.hint {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0.5rem 0;
}
h3 {
  margin: 0 0 1rem;
}
</style>
