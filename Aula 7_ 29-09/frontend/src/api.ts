import axios from 'axios'

export interface User {
  id: string
  name: string
  email: string
}

export interface AuthResponse {
  user: User
  accessToken: string
}

export interface Transcription {
  id: string
  text: string
  originalFilename: string
  createdAt: string
}

const SESSION_KEY = 'ditado.session'

export function getSession(): AuthResponse | null {
  try {
    const raw = localStorage.getItem(SESSION_KEY)
    return raw ? (JSON.parse(raw) as AuthResponse) : null
  } catch {
    return null
  }
}

export function saveSession(session: AuthResponse) {
  localStorage.setItem(SESSION_KEY, JSON.stringify(session))
}

export function clearSession() {
  localStorage.removeItem(SESSION_KEY)
}

export const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use((config) => {
  const session = getSession()
  if (session) {
    config.headers.Authorization = `Bearer ${session.accessToken}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const url: string = error.config?.url ?? ''
    if (error.response?.status === 401 && !url.startsWith('/auth')) {
      clearSession()
      window.location.href = '/'
    }
    return Promise.reject(error)
  },
)

export function errorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const message = error.response?.data?.message
    if (Array.isArray(message)) return message.join('. ')
    if (typeof message === 'string') return message
    if (error.response?.status === 413) {
      return 'Arquivo muito grande (máximo 25 MB).'
    }
    if (!error.response) return 'Não foi possível falar com o servidor.'
  }
  return 'Algo deu errado. Tente novamente.'
}