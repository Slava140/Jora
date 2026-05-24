import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiClient } from '@/api/client'

export const useCapabilitiesStore = defineStore('capabilities', () => {
  const canManageUsers = ref(false)
  const loaded = ref(false)

  async function probe(): Promise<void> {
    const hasWrite = (e: unknown) => {
      const status = (e as { response?: { status?: number } }).response?.status
      return status !== 403 && status !== 401
    }

    try {
      await apiClient.post('/api/v1/users/', {})
      canManageUsers.value = true
    } catch (e: unknown) {
      canManageUsers.value = hasWrite(e)
    }

    loaded.value = true
  }

  function reset(): void {
    canManageUsers.value = false
    loaded.value = false
  }

  return {
    canManageUsers,
    loaded,
    probe,
    reset,
  }
})
