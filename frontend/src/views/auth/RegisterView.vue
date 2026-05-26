<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useCapabilitiesStore } from '@/stores/capabilities'
import { getErrorMessage } from '@/utils/errors'
import { validatePassword } from '@/utils/password'

const auth = useAuthStore()
const caps = useCapabilitiesStore()
const router = useRouter()

const form = reactive({ username: '', email: '', password: '' })
const loading = ref(false)

async function submit() {
  const pwdErr = validatePassword(form.password)
  if (pwdErr) {
    ElMessage.warning(pwdErr)
    return
  }
  loading.value = true
  try {
    await auth.signup(form)
    caps.reset()
    await caps.probe()
    router.push('/projects')
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-brand">
      <span class="auth-logo">Jora</span>
      <p>Создайте аккаунт для работы с проектами</p>
    </div>
    <el-card class="auth-card">
      <h1>Регистрация</h1>
      <el-form label-position="top" @submit.prevent="submit">
        <el-form-item label="Имя пользователя">
          <el-input v-model="form.username" minlength="3" maxlength="255" />
        </el-form-item>
        <el-form-item label="Email">
          <el-input v-model="form.email" type="email" />
        </el-form-item>
        <el-form-item label="Пароль">
          <el-input v-model="form.password" type="password" show-password />
          <div class="hint">8–20 символов, цифра, заглавная и строчная буква</div>
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading" class="submit-btn">
          Зарегистрироваться
        </el-button>
      </el-form>
      <p class="link">
        Уже есть аккаунт? <router-link to="/login">Войти</router-link>
      </p>
    </el-card>
  </div>
</template>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--jora-bg);
  padding: 2rem;
}
.auth-brand {
  text-align: center;
  margin-bottom: 2rem;
}
.auth-logo {
  font-size: 2rem;
  font-weight: 700;
  color: var(--jora-primary);
}
.auth-brand p {
  margin: 0.5rem 0 0;
  color: var(--jora-text-muted);
  font-size: 0.875rem;
}
.auth-card {
  width: 100%;
  max-width: 400px;
}
.auth-card h1 {
  margin: 0 0 1.5rem;
  text-align: center;
  font-size: 1.25rem;
}
.hint {
  font-size: 0.75rem;
  color: var(--jora-text-muted);
  margin-top: 0.25rem;
}
.submit-btn {
  width: 100%;
}
.link {
  text-align: center;
  margin-top: 1rem;
  font-size: 0.875rem;
}
.link a {
  color: var(--jora-primary);
}
</style>
