export function getAuthToken() {
  if (typeof window !== 'undefined' && window.__APP_AUTH_TOKEN__) {
    return String(window.__APP_AUTH_TOKEN__)
  }

  if (typeof document === 'undefined') return ''

  const match = document.cookie.match(/(?:^|;\s*)app_auth_token=([^;]+)/)
  return match ? decodeURIComponent(match[1]) : ''
}

