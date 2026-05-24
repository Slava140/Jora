import { apiClient } from './client'
import type { CreateUserBody, LoggedInUser, LoginBody } from '@/types'

export async function login(body: LoginBody): Promise<LoggedInUser> {
  const { data } = await apiClient.post<LoggedInUser>('/auth/login/', body)
  return data
}

export async function signup(body: CreateUserBody): Promise<LoggedInUser> {
  const { data } = await apiClient.post<LoggedInUser>('/auth/signup/', body)
  return data
}
