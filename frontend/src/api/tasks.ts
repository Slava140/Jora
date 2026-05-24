import { apiClient } from './client'
import type {
  CreateTaskBody,
  Task,
  TaskFilters,
  TaskWithMedia,
  UpdateTaskBody,
} from '@/types'

export async function getTasks(params: TaskFilters = {}): Promise<TaskWithMedia[]> {
  const { data } = await apiClient.get<TaskWithMedia[]>('/api/v1/tasks/', { params })
  return data
}

export async function getTaskById(taskId: number): Promise<TaskWithMedia> {
  const { data } = await apiClient.get<TaskWithMedia>(`/api/v1/tasks/${taskId}/`)
  return data
}

export async function createTask(body: CreateTaskBody): Promise<Task> {
  const { data } = await apiClient.post<Task>('/api/v1/tasks/', body)
  return data
}

export async function updateTask(taskId: number, body: UpdateTaskBody): Promise<Task> {
  const { data } = await apiClient.put<Task>(`/api/v1/tasks/${taskId}/`, body)
  return data
}

export async function deleteTask(taskId: number): Promise<void> {
  await apiClient.delete(`/api/v1/tasks/${taskId}/`)
}
