<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import AppShell from '@/components/layout/AppShell.vue'
import PageHeader from '@/components/common/PageHeader.vue'
import TaskStatusBadge from '@/components/tasks/TaskStatusBadge.vue'
import CommentList from '@/components/CommentList.vue'
import MediaGallery from '@/components/MediaGallery.vue'
import MediaUpload from '@/components/MediaUpload.vue'
import * as tasksApi from '@/api/tasks'
import * as projectsApi from '@/api/projects'
import * as usersApi from '@/api/users'
import { useAuthStore } from '@/stores/auth'
import { formatDisplayDatetime, parseApiDatetime, formatApiDatetime } from '@/utils/datetime'
import { getErrorMessage } from '@/utils/errors'
import type { Project, TaskStatus, TaskWithMedia, User } from '@/types'

const props = defineProps<{ projectId: string; taskId: string }>()
const router = useRouter()
const auth = useAuthStore()

const projectIdNum = computed(() => parseInt(props.projectId, 10))
const taskIdNum = computed(() => parseInt(props.taskId, 10))

const task = ref<TaskWithMedia | null>(null)
const project = ref<Project | null>(null)
const projectUsers = ref<User[]>([])
const loading = ref(false)
const saving = ref(false)

const editStatus = ref<TaskStatus>('open')
const editAssignee = ref<number | null>(null)
const editDescription = ref('')
const editDueDateTs = ref<number | null>(null)
const savingDescription = ref(false)

function buildUpdateBody(
  overrides: Partial<{
    status: TaskStatus
    assignee_id: number | null
    description: string
    due_date: string | null
  }> = {},
) {
  return {
    status: overrides.status ?? editStatus.value,
    assignee_id:
      overrides.assignee_id !== undefined ? overrides.assignee_id : editAssignee.value,
    description: overrides.description ?? editDescription.value,
    due_date:
      overrides.due_date !== undefined
        ? overrides.due_date
        : editDueDateTs.value !== null
          ? formatApiDatetime(new Date(editDueDateTs.value))
          : null,
  }
}

const usersMap = computed(() => {
  const map = Object.fromEntries(projectUsers.value.map((u) => [u.id, u.username]))
  if (task.value && !map[task.value.author_id]) {
    map[task.value.author_id] = `User #${task.value.author_id}`
  }
  return map
})

const galleryRef = ref<InstanceType<typeof MediaGallery> | null>(null)

const canDelete = computed(() => {
  if (!task.value || !auth.user) return false
  return task.value.author_id === auth.user.id
})

async function load() {
  loading.value = true
  try {
    const [t, p, u] = await Promise.all([
      tasksApi.getTaskById(taskIdNum.value),
      projectsApi.getProjectById(projectIdNum.value),
      projectsApi.getProjectUsers(projectIdNum.value),
    ])
    if (t.project_id !== projectIdNum.value) {
      router.replace(`/projects/${t.project_id}/tasks/${t.id}`)
      return
    }
    const users = [...u]
    const knownIds = new Set(users.map((x) => x.id))
    for (const uid of [t.author_id, t.assignee_id]) {
      if (uid && !knownIds.has(uid)) {
        try {
          const user = await usersApi.getUserById(uid)
          users.push(user)
          knownIds.add(uid)
        } catch {
          /* ignore */
        }
      }
    }
    task.value = t
    project.value = p
    projectUsers.value = users
    editStatus.value = t.status
    editAssignee.value = t.assignee_id
    editDescription.value = t.description ?? ''
    editDueDateTs.value = t.due_date ? parseApiDatetime(t.due_date).getTime() : null
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
    router.push(`/projects/${projectIdNum.value}`)
  } finally {
    loading.value = false
  }
}

async function saveUpdate() {
  if (!task.value) return
  saving.value = true
  try {
    const updated = await tasksApi.updateTask(taskIdNum.value, buildUpdateBody())
    task.value = { ...task.value, ...updated, media: task.value.media }
    ElMessage.success('Задача обновлена')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    saving.value = false
  }
}

async function saveDescription() {
  if (!task.value) return
  savingDescription.value = true
  try {
    const updated = await tasksApi.updateTask(
      taskIdNum.value,
      buildUpdateBody({
        status: task.value.status,
        assignee_id: task.value.assignee_id,
        description: editDescription.value,
      }),
    )
    task.value = { ...task.value, ...updated, media: task.value.media }
    ElMessage.success('Описание сохранено')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    savingDescription.value = false
  }
}

async function quickStatus(status: TaskStatus) {
  editStatus.value = status
  await saveUpdate()
}

async function remove() {
  await ElMessageBox.confirm('Удалить задачу?', 'Подтверждение', { type: 'warning' })
  try {
    await tasksApi.deleteTask(taskIdNum.value)
    ElMessage.success('Задача удалена')
    router.push(`/projects/${projectIdNum.value}`)
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
  <AppShell>
    <div v-loading="loading" class="task-detail">
      <template v-if="task && project">
        <PageHeader :title="task.title">
          <template #breadcrumbs>
            <router-link to="/projects">Проекты</router-link>
            <span> / </span>
            <router-link :to="`/projects/${projectIdNum}`">{{ project.title }}</router-link>
            <span> / JORA-{{ task.id }}</span>
          </template>
          <template #actions>
            <el-button @click="router.push(`/projects/${projectIdNum}`)">К доске</el-button>
          </template>
        </PageHeader>

        <div class="task-layout">
          <div class="task-main">
            <section class="jora-card section">
              <div class="section-head">
                <h2>Описание</h2>
                <TaskStatusBadge :status="task.status" />
              </div>
              <el-input
                v-model="editDescription"
                type="textarea"
                :rows="6"
                placeholder="Добавьте описание задачи"
              />
              <el-button
                type="primary"
                class="save-description"
                :loading="savingDescription"
                @click="saveDescription"
              >
                Сохранить описание
              </el-button>
            </section>

            <section class="jora-card section">
              <h2>Детали</h2>
              <dl class="meta-grid">
                <dt>Ключ</dt>
                <dd>JORA-{{ task.id }}</dd>
                <dt>Автор</dt>
                <dd>{{ usersMap[task.author_id] ?? task.author_id }}</dd>
                <dt>Исполнитель</dt>
                <dd>
                  {{ task.assignee_id ? usersMap[task.assignee_id] ?? task.assignee_id : '—' }}
                </dd>
                <dt>Срок</dt>
                <dd>{{ formatDisplayDatetime(task.due_date) }}</dd>
                <dt>Создана</dt>
                <dd>{{ formatDisplayDatetime(task.created_at) }}</dd>
                <dt>Обновлена</dt>
                <dd>{{ formatDisplayDatetime(task.updated_at) }}</dd>
              </dl>
            </section>

            <section class="jora-card section">
              <MediaUpload :task-id="taskIdNum" @uploaded="onMediaUploaded" />
              <MediaGallery ref="galleryRef" :media="task.media ?? []" />
            </section>

            <section class="jora-card section">
              <CommentList :task-id="taskIdNum" :users-map="usersMap" />
            </section>
          </div>

          <aside class="task-sidebar jora-card">
            <h3>Операции</h3>
            <el-form label-position="top" @submit.prevent="saveUpdate">
              <el-form-item label="Статус">
                <el-select v-model="editStatus" style="width: 100%">
                  <el-option label="Открыта" value="open" />
                  <el-option label="В работе" value="in_progress" />
                  <el-option label="Завершена" value="finished" />
                </el-select>
              </el-form-item>
              <el-form-item label="Исполнитель">
                <el-select
                  v-model="editAssignee"
                  clearable
                  placeholder="Не назначен"
                  style="width: 100%"
                >
                  <el-option
                    v-for="u in projectUsers"
                    :key="u.id"
                    :label="u.username"
                    :value="u.id"
                  />
                </el-select>
              </el-form-item>
              <el-form-item label="Срок выполнения">
                <el-date-picker
                  v-model="editDueDateTs"
                  type="datetime"
                  value-format="x"
                  placeholder="Не указан"
                  clearable
                  style="width: 100%"
                />
              </el-form-item>
              <el-button type="primary" native-type="submit" :loading="saving" style="width: 100%">
                Сохранить
              </el-button>
            </el-form>

            <div class="quick-actions">
              <el-button size="small" @click="quickStatus('in_progress')">В работу</el-button>
              <el-button size="small" type="success" @click="quickStatus('finished')">
                Завершить
              </el-button>
            </div>

            <p class="hint">
              Редактировать могут автор, исполнитель или владелец проекта.
            </p>

            <el-button v-if="canDelete" type="danger" plain style="width: 100%" @click="remove">
              Удалить задачу
            </el-button>
          </aside>
        </div>
      </template>
    </div>
  </AppShell>
</template>

<style scoped>
.task-layout {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 1.5rem;
  align-items: start;
}
@media (max-width: 900px) {
  .task-layout {
    grid-template-columns: 1fr;
  }
}
.section {
  padding: 1.25rem;
  margin-bottom: 1rem;
}
.section h2 {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 600;
}
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}
.section-head h2 {
  margin: 0;
}
.save-description {
  margin-top: 0.75rem;
}
.meta-grid {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 0.5rem 1rem;
  margin: 0;
}
.meta-grid dt {
  color: var(--jora-text-muted);
  font-size: 0.875rem;
}
.meta-grid dd {
  margin: 0;
}
.task-sidebar {
  padding: 1.25rem;
  position: sticky;
  top: 72px;
}
.task-sidebar h3 {
  margin: 0 0 1rem;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  color: var(--jora-text-muted);
}
.quick-actions {
  display: flex;
  gap: 0.5rem;
  margin: 1rem 0;
  flex-wrap: wrap;
}
.hint {
  font-size: 0.75rem;
  color: var(--jora-text-muted);
  margin: 0 0 1rem;
}
</style>
