import type { AxiosError } from 'axios'
import type { ApiError, ValidationErrorItem } from '@/types'

export function getErrorMessage(error: unknown): string {
  if (!error || typeof error !== 'object') return 'Неизвестная ошибка'
  const ax = error as AxiosError<ApiError | ValidationErrorItem[]>
  const data = ax.response?.data
  if (!data) return ax.message || 'Сетевая ошибка'
  if (Array.isArray(data)) {
    return data.map((e) => `${e.loc?.join('.') ?? 'field'}: ${e.msg}`).join('; ')
  }
  if (typeof data === 'object' && 'message' in data) {
    return (data as ApiError).message
  }
  return ax.message || 'Ошибка запроса'
}

export function getValidationErrors(error: unknown): Record<string, string> {
  const ax = error as AxiosError<ValidationErrorItem[]>
  const data = ax.response?.data
  if (!Array.isArray(data)) return {}
  const result: Record<string, string> = {}
  for (const item of data) {
    const key = item.loc?.[item.loc.length - 1] ?? 'form'
    result[key] = item.msg
  }
  return result
}
