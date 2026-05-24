import { apiClient } from '@/api/client'

export function extractMediaId(url: string): number | null {
  const m = url.match(/\/media\/(\d+)\//)
  return m ? parseInt(m[1], 10) : null
}

export async function fetchAuthenticatedBlob(
  mediaId: number,
  original = false,
): Promise<Blob> {
  const response = await apiClient.get(`/media/${mediaId}/`, {
    params: { original },
    responseType: 'blob',
  })
  return response.data as Blob
}

export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}
