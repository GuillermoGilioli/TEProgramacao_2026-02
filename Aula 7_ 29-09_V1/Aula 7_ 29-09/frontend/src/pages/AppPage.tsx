import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import { api, clearSession, errorMessage, getSession } from '../api'
import type { Transcription } from '../api'

const MAX_BYTES = 25 * 1024 * 1024
const ACCEPT = '.mp3,.m4a,.wav,.ogg,.webm,.flac,.mp4,.mpeg'

export default function AppPage() {
  const navigate = useNavigate()
  const session = getSession()
  const hasSession = Boolean(session)
  const [items, setItems] = useState<Transcription[]>([])
  const [file, setFile] = useState<File | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [loadingList, setLoadingList] = useState(true)

  useEffect(() => {
    if (!hasSession) return
    api
      .get<Transcription[]>('/transcriptions')
      .then((res) => setItems(res.data))
      .catch((err) => setError(errorMessage(err)))
      .finally(() => setLoadingList(false))
  }, [hasSession])

  if (!session) {
    return <Navigate to="/" replace />
  }

  function logout() {
    clearSession()
    navigate('/', { replace: true })
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const formElement = event.currentTarget
    if (!file) {
      setError('Escolha um arquivo de áudio.')
      return
    }
    if (file.size > MAX_BYTES) {
      setError('Arquivo muito grande (máximo 25 MB).')
      return
    }
    setError('')
    setLoading(true)
    try {
      const form = new FormData()
      form.append('file', file)
      const { data } = await api.post<Transcription>('/transcriptions', form)
      setItems((current) => [data, ...current])
      setFile(null)
      formElement.reset()
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="app">
      <header>
        <h1>Ditado</h1>
        <div className="user">
          <span>{session.user.name}</span>
          <button type="button" className="secondary" onClick={logout}>
            Sair
          </button>
        </div>
      </header>

      <form onSubmit={handleSubmit} className="card">
        <h2>Nova transcrição</h2>
        <input
          type="file"
          accept={ACCEPT}
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <p className="muted small">
          Formatos: mp3, m4a, wav, ogg, webm, flac, mp4, mpeg. Até 25 MB.
        </p>
        {error && <p className="error">{error}</p>}
        <button type="submit" disabled={loading || !file}>
          {loading ? 'Transcrevendo...' : 'Transcrever'}
        </button>
      </form>

      <section>
        <h2>Histórico</h2>
        {loadingList ? (
          <p className="muted">Carregando...</p>
        ) : items.length === 0 ? (
          <p className="muted">Nenhuma transcrição ainda.</p>
        ) : (
          <ul className="list">
            {items.map((item) => (
              <li key={item.id} className="card">
                <div className="meta">
                  <strong>{item.originalFilename}</strong>
                  <span className="muted small">
                    {new Date(item.createdAt).toLocaleString('pt-BR')}
                  </span>
                </div>
                <p className="text">{item.text}</p>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  )
}