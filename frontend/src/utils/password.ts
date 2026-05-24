export function validatePassword(password: string): string | null {
  if (password.length < 8) return 'Минимум 8 символов'
  if (password.length > 20) return 'Максимум 20 символов'
  if (!/\d/.test(password)) return 'Нужна хотя бы одна цифра'
  if (!/[A-Z]/.test(password)) return 'Нужна хотя бы одна заглавная буква'
  if (!/[a-z]/.test(password)) return 'Нужна хотя бы одна строчная буква'
  return null
}
