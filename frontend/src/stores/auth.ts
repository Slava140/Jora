import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '@/api/auth'
import { setAuthToken, setUnauthorizedHandler } from '@/api/client'
import type { CreateUserBody, LoggedInUser, LoginBody, User } from '@/types'

const STORAGE_KEY = 'jora_auth'

interface StoredAuth {
  user: User
  access_token: string
}

function loadStored(): StoredAuth | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as StoredAuth) : null
  } catch {
    return null
  }
}

function saveStored(user: User, token: string): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ user, access_token: token }))
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)

  const isAuthenticated = computed(() => !!accessToken.value)

  function applySession(loggedIn: LoggedInUser): void {
    const { access_token, ...userData } = loggedIn
    user.value = userData
    accessToken.value = access_token
    setAuthToken(access_token)
    saveStored(userData, access_token)
  }

  function clearSession(): void {
    user.value = null
    accessToken.value = null
    setAuthToken(null)
    localStorage.removeItem(STORAGE_KEY)
  }

  function init(): void {
    setUnauthorizedHandler(() => clearSession())
    const stored = loadStored()
    if (stored) {
      user.value = stored.user
      accessToken.value = stored.access_token
      setAuthToken(stored.access_token)
    }
  }

  async function login(body: LoginBody): Promise<void> {
    const data = await authApi.login(body)
    applySession(data)
  }

  async function signup(body: CreateUserBody): Promise<void> {
    const data = await authApi.signup(body)
    applySession(data)
  }

  function logout(): void {
    clearSession()
  }

  return {
    user,
    accessToken,
    isAuthenticated,
    init,
    login,
    signup,
    logout,
  }
})
