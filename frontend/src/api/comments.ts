import { apiClient } from './client'
import type { Comment, CommentFilters, CreateCommentBody } from '@/types'

export async function getComments(params: CommentFilters = {}): Promise<Comment[]> {
  const { data } = await apiClient.get<Comment[]>('/api/v1/comments/', { params })
  return data
}

export async function getCommentById(commentId: number): Promise<Comment> {
  const { data } = await apiClient.get<Comment>(`/api/v1/comments/${commentId}/`)
  return data
}

export async function createComment(body: CreateCommentBody): Promise<Comment> {
  const { data } = await apiClient.post<Comment>('/api/v1/comments/', body)
  return data
}
