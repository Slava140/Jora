<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useCapabilitiesStore } from '@/stores/capabilities'
import { getErrorMessage } from '@/utils/errors'

const auth = useAuthStore()
const caps = useCapabilitiesStore()
const router = useRouter()
const route = useRoute()

const form = reactive({ email: '', password: '' })
const loading = ref(false)

async function submit() {
  loading.value = true
  try {
    await auth.login(form)
    caps.reset()
    await caps.probe()
    const redirect = (route.query.redirect as string) || '/projects'
    router.push(redirect)
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
      <p>Управление проектами и задачами</p>
    </div>
    <el-card class="auth-card">
      <h1>Вход</h1>
      <el-form label-position="top" @submit.prevent="submit">
        <el-form-item label="Email">
          <el-input v-model="form.email" type="email" autocomplete="email" />
        </el-form-item>
        <el-form-item label="Пароль">
          <el-input
            v-model="form.password"
            type="password"
            show-password
            autocomplete="current-password"
          />
        </el-form-item>
        <el-button type="primary" native-type="submit" :loading="loading" class="submit-btn">
          Войти
        </el-button>
      </el-form>
      <p class="link">
        Нет аккаунта? <router-link to="/register">Регистрация</router-link>
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
