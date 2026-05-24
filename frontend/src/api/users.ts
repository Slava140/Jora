import { apiClient } from './client'
import type {
  CreateUserBody,
  PaginationParams,
  UpdateUserBody,
  User,
} from '@/types'

export async function getUsers(params: PaginationParams = {}): Promise<User[]> {
  const { data } = await apiClient.get<User[]>('/api/v1/users/', { params })
  return data
}

export async function getUserById(userId: number): Promise<User> {
  const { data } = await apiClient.get<User>(`/api/v1/users/${userId}/`)
  return data
}

export async function createUser(body: CreateUserBody): Promise<User> {
  const { data } = await apiClient.post<User>('/api/v1/users/', body)
  return data
}

export async function updateUser(userId: number, body: UpdateUserBody): Promise<User> {
  const { data } = await apiClient.put<User>(`/api/v1/users/${userId}/`, body)
  return data
}

export async function deleteUser(userId: number): Promise<void> {
  await apiClient.delete(`/api/v1/users/${userId}/`)
}
