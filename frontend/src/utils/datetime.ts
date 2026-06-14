const API_DATETIME_RE = /^(\d{2})\.(\d{2})\.(\d{4}) (\d{2}):(\d{2}):(\d{2})([+-]\d{4})$/

export function parseApiDatetime(value: string): Date {
  const m = value.match(API_DATETIME_RE)
  if (!m) return new Date(value)
  const [, dd, mm, yyyy, hh, min, sec, tz] = m
  const tzSign = tz[0] === '+' ? 1 : -1
  const tzHours = parseInt(tz.slice(1, 3), 10)
  const tzMins = parseInt(tz.slice(3, 5), 10)
  const offsetMinutes = tzSign * (tzHours * 60 + tzMins)
  const utcMs = Date.UTC(
    parseInt(yyyy, 10),
    parseInt(mm, 10) - 1,
    parseInt(dd, 10),
    parseInt(hh, 10),
    parseInt(min, 10),
    parseInt(sec, 10),
  ) - offsetMinutes * 60 * 1000
  return new Date(utcMs)
}

export function formatApiDatetime(date: Date): string {
  const pad = (n: number) => String(n).padStart(2, '0')
  const offsetMin = -date.getTimezoneOffset()
  const sign = offsetMin >= 0 ? '+' : '-'
  const abs = Math.abs(offsetMin)
  const tz = `${sign}${pad(Math.floor(abs / 60))}${pad(abs % 60)}`
  return `${pad(date.getDate())}.${pad(date.getMonth() + 1)}.${date.getFullYear()} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}${tz}`
}

export function toApiDatetime(value: string | null): string | null {
  if (!value) return null
  return formatApiDatetime(parseApiDatetime(value))
}

export function formatDisplayDatetime(value: string | null): string {
  if (!value) return '—'
  try {
    return parseApiDatetime(value).toLocaleString('ru-RU')
  } catch {
    return value
  }
}

export function toDateInputValue(value: string | null): string {
  if (!value) return ''
  const d = parseApiDatetime(value)
  return d.toISOString().slice(0, 16)
}

export function fromDateInputValue(value: string): string | null {
  if (!value) return null
  return formatApiDatetime(new Date(value))
}

export function toDateFilterValue(value: string | undefined): string | undefined {
  if (!value) return undefined
  const d = new Date(value)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}
