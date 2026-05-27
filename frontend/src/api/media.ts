import { apiClient } from './client'
import type { Media } from '@/types'

export async function uploadMedia(file: File, taskId: number): Promise<Media> {
  const form = new FormData()
  form.append('file', file)
  form.append('compress_it', 'false')
  form.append('task_id', String(taskId))
  const { data } = await apiClient.post<Media>('/media/', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}
