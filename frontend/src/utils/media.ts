import type { TaskMedia } from '@/types'

/** One entry per file (API may return original + compressed as separate rows). */
export function uniqueTaskMedia(media: TaskMedia[] | undefined | null): TaskMedia[] {
  if (!media?.length) return []
  const byId = new Map<number, TaskMedia>()
  for (const item of media) {
    if (!byId.has(item.id)) {
      byId.set(item.id, item)
    }
  }
  return Array.from(byId.values())
}

export function taskMediaCount(media: TaskMedia[] | undefined | null): number {
  return uniqueTaskMedia(media).length
}
