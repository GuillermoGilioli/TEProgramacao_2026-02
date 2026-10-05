import { useState } from 'react'
import type { FormEvent } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { api, errorMessage, getSession, saveSession } from '../api'
import type { AuthResponse } from '../api'

const PASSWORD_RULES = [
  { label: 'Pelo menos 8 caracteres', test: (v: string) => v.length >= 8 },
  { label: 'Uma letra maiúscula', test: (v: string) => /[A-Z]/.test(v) },
  { label: 'Uma letra minúscula', test: (v: string) => /[a-z]/.test(v) },
  { label: 'Um número', test: (v: string) => /\d/.test(v) },
  {
    label: 'Um caractere especial (ex.: ! @ # $ %)',
    test: (v: string) => /[^A-Za-z0-9]/.test(v),
  },
]

export default function AuthPage() {
  const navigate = useNavigate()
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (getSession()) {
    return <Navigate to="/app" replace />
  }

  const passwordOk = PASSWORD_RULES.every((rule) => rule.test(password))

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    if (mode === 'register' && !passwordOk) {
      setError('A senha não atende a todos os requisitos.')
      return
    }
    setError('')
    setLoading(true)
    try {
      const body =
        mode === 'register' ? { name, email, password } : { email, password }
      const { data } = await api.post<AuthResponse>(`/auth/${mode}`, body)
      saveSession(data)
      navigate('/app', { replace: true })
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth">
      <h1>Ditado</h1>
      <p className="muted">Envie um áudio e receba o texto transcrito.</p>

      <div className="tabs">
        <button
          type="button"
          className={mode === 'login' ? 'tab active' : 'tab'}
          onClick={() => setMode('login')}
        >
          Entrar
        </button>
        <button
          type="button"
          className={mode === 'register' ? 'tab active' : 'tab'}
          onClick={() => setMode('register')}
        >
          Criar conta
        </button>
      </div>

      <form onSubmit={handleSubmit} className="card">
        {mode === 'register' && (
          <label>
            Nome
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              minLength={2}
              maxLength={100}
            />
          </label>
        )}
        <label>
          E-mail
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        <label>
          Senha
          <div className="password-field">
            <input
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button
              type="button"
              className="toggle"
              onClick={() => setShowPassword((current) => !current)}
              aria-label={showPassword ? 'Ocultar senha' : 'Mostrar senha'}
              aria-pressed={showPassword}
            >
              {showPassword ? 'Ocultar' : 'Mostrar'}
            </button>
          </div>
        </label>
        {mode === 'register' && (
          <ul className="rules">
            {PASSWORD_RULES.map((rule) => {
              const ok = rule.test(password)
              return (
                <li key={rule.label} className={ok ? 'rule ok' : 'rule'}>
                  <span aria-hidden="true">{ok ? '✓' : '○'}</span> {rule.label}
                </li>
              )
            })}
          </ul>
        )}
        {error && <p className="error">{error}</p>}
        <button
          type="submit"
          disabled={loading || (mode === 'register' && !passwordOk)}
        >
          {loading ? 'Aguarde...' : mode === 'login' ? 'Entrar' : 'Criar conta'}
        </button>
      </form>
    </main>
  )
}