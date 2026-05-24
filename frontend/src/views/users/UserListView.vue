<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AppLayout from '@/components/AppLayout.vue'
import PaginationBar from '@/components/PaginationBar.vue'
import * as usersApi from '@/api/users'
import { formatDisplayDatetime } from '@/utils/datetime'
import { getErrorMessage } from '@/utils/errors'
import type { User } from '@/types'

const router = useRouter()
const users = ref<User[]>([])
const loading = ref(false)
const page = ref(1)
const limit = ref(10)

async function load() {
  loading.value = true
  try {
    users.value = await usersApi.getUsers({ page: page.value, limit: limit.value })
  } catch (e) {
    ElMessage.error(getErrorMessage(e))
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <AppLayout>
    <div class="page-header">
      <h1>Пользователи</h1>
      <el-button type="primary" @click="router.push('/users/new')">Создать</el-button>
    </div>

    <el-table v-loading="loading" :data="users" stripe>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="username" label="Имя" />
      <el-table-column prop="email" label="Email" />
      <el-table-column label="Создан">
        <template #default="{ row }">{{ formatDisplayDatetime(row.create_datetime) }}</template>
      </el-table-column>
      <el-table-column label="" width="120">
        <template #default="{ row }">
          <el-button text type="primary" @click="router.push(`/users/${row.id}/edit`)">
            Редактировать
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <PaginationBar v-model:page="page" v-model:limit="limit" @change="load" />
  </AppLayout>
</template>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.page-header h1 {
  margin: 0;
}
</style>
