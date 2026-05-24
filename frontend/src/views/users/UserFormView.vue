<script setup lang="ts">
import { reactive, ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import AppLayout from '@/components/AppLayout.vue'
import * as usersApi from '@/api/users'
import { getErrorMessage } from '@/utils/errors'
import { validatePassword } from '@/utils/password'

const props = defineProps<{ id?: string }>()
const route = useRoute()
const router = useRouter()

const userId = computed(() => {
  const raw = props.id ?? route.params.id
  return raw ? parseInt(String(raw), 10) : null
})
const isEdit = computed(() => userId.value != null)

const form = reactive({ username: '', email: '', password: '' })
const loading = ref(false)
const saving = ref(false)

async function load() {
  if (!userId.value) return
  loading.value = true
  try {
    const u = await usersApi.getUserById(userId.value)
    form.username = u.username
    form.email = u.email
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
    router.push('/users')
  } finally {
    loading.value = false
  }
}

async function save() {
  saving.value = true
  try {
    if (isEdit.value && userId.value) {
      await usersApi.updateUser(userId.value, {
        username: form.username,
        email: form.email,
      })
      ElMessage.success('Пользователь обновлён')
      router.push('/users')
    } else {
      const pwdErr = validatePassword(form.password)
      if (pwdErr) {
        ElMessage.warning(pwdErr)
        return
      }
      await usersApi.createUser({
        username: form.username,
        email: form.email,
        password: form.password,
      })
      ElMessage.success('Пользователь создан')
      router.push('/users')
    }
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    saving.value = false
  }
}

async function remove() {
  if (!userId.value) return
  await ElMessageBox.confirm('Удалить пользователя?', 'Подтверждение', { type: 'warning' })
  try {
    await usersApi.deleteUser(userId.value)
    ElMessage.success('Пользователь удалён')
    router.push('/users')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <el-card v-loading="loading">
      <h1>{{ isEdit ? 'Редактирование пользователя' : 'Новый пользователь' }}</h1>
      <el-form label-position="top" @submit.prevent="save">
        <el-form-item label="Имя пользователя" required>
          <el-input v-model="form.username" minlength="3" maxlength="255" />
        </el-form-item>
        <el-form-item label="Email" required>
          <el-input v-model="form.email" type="email" />
        </el-form-item>
        <el-form-item v-if="!isEdit" label="Пароль" required>
          <el-input v-model="form.password" type="password" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="saving">Сохранить</el-button>
          <el-button @click="router.back()">Отмена</el-button>
          <el-button v-if="isEdit" type="danger" @click="remove">Удалить</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </AppLayout>
</template>

<style scoped>
h1 {
  margin: 0 0 1rem;
}
</style>
