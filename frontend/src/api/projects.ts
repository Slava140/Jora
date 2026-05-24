import { apiClient } from './client'
import type { CreateProjectBody, PaginationParams, Project } from '@/types'

export async function getProjects(params: PaginationParams = {}): Promise<Project[]> {
  const { data } = await apiClient.get<Project[]>('/api/v1/projects/', { params })
  return data
}

export async function getProjectById(projectId: number): Promise<Project> {
  const { data } = await apiClient.get<Project>(`/api/v1/projects/${projectId}/`)
  return data
}

export async function createProject(body: CreateProjectBody): Promise<Project> {
  const { data } = await apiClient.post<Project>('/api/v1/projects/', body)
  return data
}

export async function updateProject(
  projectId: number,
  body: CreateProjectBody,
): Promise<Project> {
  const { data } = await apiClient.put<Project>(`/api/v1/projects/${projectId}/`, body)
  return data
}

export async function deleteProject(projectId: number): Promise<void> {
  await apiClient.delete(`/api/v1/projects/${projectId}/`)
}

export async function exportProject(projectId: number): Promise<Blob> {
  const { data } = await apiClient.get(`/api/v1/projects/${projectId}/export/`, {
    responseType: 'blob',
  })
  return data as Blob
}

export async function importProject(file: File): Promise<void> {
  const form = new FormData()
  form.append('file', file)
  await apiClient.post('/api/v1/projects/import/', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}
