import { useCallback, useEffect, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? '/api'

type AirflowHealth = {
  configured: boolean
  status: string
  detail: {
    metadatabase?: { status: string }
    scheduler?: { status: string; latest_scheduler_heartbeat: string | null }
  }
}

type AirflowDag = {
  dag_id: string
  is_active: boolean
  is_paused: boolean
  last_parsed_time: string | null
  next_dagrun: string | null
  description: string | null
}

type AirflowDagsResponse = {
  total: number
  dags: AirflowDag[]
}

type TriggerResult = {
  dag_id: string
  run_id: string
  state: string
}

function StatusBadge({ ok, label }: { ok: boolean; label: string }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold ${
        ok ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
      }`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${ok ? 'bg-emerald-500' : 'bg-red-500'}`} />
      {label}
    </span>
  )
}

const ARCHITECTURE_LAYERS = [
  {
    color: 'bg-amber-50 border-amber-200',
    badge: 'bg-amber-100 text-amber-800',
    title: 'Bronze — Ingesta raw',
    description: 'Archivos CSV/XLSX subidos via portal o API. Se almacenan sin transformar.',
    icon: '📥',
  },
  {
    color: 'bg-sky-50 border-sky-200',
    badge: 'bg-sky-100 text-sky-800',
    title: 'Silver — Limpieza',
    description: 'Estandarización de columnas, manejo de nulos, tipos de datos correctos.',
    icon: '🔧',
  },
  {
    color: 'bg-violet-50 border-violet-200',
    badge: 'bg-violet-100 text-violet-800',
    title: 'Gold — Star Schema',
    description: 'Dimensiones y tabla de hechos cargadas en PostgreSQL para consumo BI.',
    icon: '⭐',
  },
  {
    color: 'bg-emerald-50 border-emerald-200',
    badge: 'bg-emerald-100 text-emerald-800',
    title: 'Power BI',
    description: 'Reportes embebidos conectados directamente al modelo estrella en Postgres.',
    icon: '📊',
  },
]

export function AdminPage() {
  const [health, setHealth] = useState<AirflowHealth | null>(null)
  const [healthError, setHealthError] = useState<string | null>(null)
  const [dags, setDags] = useState<AirflowDagsResponse | null>(null)
  const [dagsError, setDagsError] = useState<string | null>(null)
  const [loadingHealth, setLoadingHealth] = useState(true)
  const [loadingDags, setLoadingDags] = useState(true)
  const [triggerState, setTriggerState] = useState<Record<string, 'idle' | 'loading' | TriggerResult>>({})

  const fetchHealth = useCallback(async () => {
    setLoadingHealth(true)
    setHealthError(null)
    try {
      const response = await fetch(`${API_BASE}/airflow/health`)
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      setHealth(await response.json())
    } catch (error) {
      setHealthError(error instanceof Error ? error.message : 'Error desconocido')
    } finally {
      setLoadingHealth(false)
    }
  }, [])

  const fetchDags = useCallback(async () => {
    setLoadingDags(true)
    setDagsError(null)
    try {
      const response = await fetch(`${API_BASE}/airflow/dags`)
      if (!response.ok) {
        const body = await response.json().catch(() => ({}))
        throw new Error(body.detail ?? `HTTP ${response.status}`)
      }
      setDags(await response.json())
    } catch (error) {
      setDagsError(error instanceof Error ? error.message : 'Error desconocido')
    } finally {
      setLoadingDags(false)
    }
  }, [])

  useEffect(() => {
    fetchHealth()
    fetchDags()
  }, [fetchHealth, fetchDags])

  const handleTrigger = async (dagId: string) => {
    setTriggerState((prev) => ({ ...prev, [dagId]: 'loading' }))
    try {
      const response = await fetch(`${API_BASE}/airflow/dags/${dagId}/runs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({}),
      })
      if (!response.ok) {
        const body = await response.json().catch(() => ({}))
        throw new Error(body.detail ?? `HTTP ${response.status}`)
      }
      const result: TriggerResult = await response.json()
      setTriggerState((prev) => ({ ...prev, [dagId]: result }))
      setTimeout(() => setTriggerState((prev) => ({ ...prev, [dagId]: 'idle' })), 6000)
    } catch (error) {
      const msg = error instanceof Error ? error.message : 'Error'
      setTriggerState((prev) => ({ ...prev, [dagId]: { dag_id: dagId, run_id: '', state: `Error: ${msg}` } }))
      setTimeout(() => setTriggerState((prev) => ({ ...prev, [dagId]: 'idle' })), 6000)
    }
  }

  return (
    <section className="space-y-8">
      {/* ── Arquitectura ───────────────────────────────────────────────── */}
      <div>
        <h3 className="mb-1 text-base font-semibold text-slate-800">Arquitectura del Pipeline</h3>
        <p className="mb-4 text-sm text-slate-500">Flujo de datos desde la ingesta hasta la visualización.</p>
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {ARCHITECTURE_LAYERS.map((layer) => (
            <div key={layer.title} className={`rounded-2xl border p-4 ${layer.color}`}>
              <span className="text-2xl">{layer.icon}</span>
              <span className={`mt-2 inline-block rounded-full px-2 py-0.5 text-xs font-semibold ${layer.badge}`}>
                {layer.title}
              </span>
              <p className="mt-2 text-xs text-slate-600">{layer.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* ── Salud Airflow ──────────────────────────────────────────────── */}
      <div>
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-base font-semibold text-slate-800">Estado de Airflow</h3>
          <button
            type="button"
            onClick={fetchHealth}
            disabled={loadingHealth}
            className="rounded-lg border border-slate-200 px-3 py-1 text-xs font-medium text-slate-600 transition hover:bg-slate-50 disabled:opacity-50"
          >
            {loadingHealth ? 'Actualizando…' : 'Actualizar'}
          </button>
        </div>

        {healthError ? (
          <p className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">{healthError}</p>
        ) : loadingHealth ? (
          <div className="h-20 animate-pulse rounded-xl bg-slate-100" />
        ) : health ? (
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            <div className="rounded-xl border border-slate-200 bg-white p-4">
              <p className="text-xs text-slate-500">Configurado</p>
              <div className="mt-1.5">
                <StatusBadge ok={health.configured} label={health.configured ? 'Sí' : 'No'} />
              </div>
            </div>
            <div className="rounded-xl border border-slate-200 bg-white p-4">
              <p className="text-xs text-slate-500">Estado general</p>
              <div className="mt-1.5">
                <StatusBadge ok={health.status === 'ok'} label={health.status} />
              </div>
            </div>
            <div className="rounded-xl border border-slate-200 bg-white p-4">
              <p className="text-xs text-slate-500">Metabase</p>
              <div className="mt-1.5">
                <StatusBadge
                  ok={health.detail?.metadatabase?.status === 'healthy'}
                  label={health.detail?.metadatabase?.status ?? '—'}
                />
              </div>
            </div>
            <div className="rounded-xl border border-slate-200 bg-white p-4">
              <p className="text-xs text-slate-500">Scheduler</p>
              <div className="mt-1.5">
                <StatusBadge
                  ok={health.detail?.scheduler?.status === 'healthy'}
                  label={health.detail?.scheduler?.status ?? '—'}
                />
              </div>
            </div>
          </div>
        ) : null}
      </div>

      {/* ── DAGs ───────────────────────────────────────────────────────── */}
      <div>
        <div className="mb-3 flex items-center justify-between">
          <h3 className="text-base font-semibold text-slate-800">
            DAGs registrados
            {dags && (
              <span className="ml-2 rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600">
                {dags.total}
              </span>
            )}
          </h3>
          <button
            type="button"
            onClick={fetchDags}
            disabled={loadingDags}
            className="rounded-lg border border-slate-200 px-3 py-1 text-xs font-medium text-slate-600 transition hover:bg-slate-50 disabled:opacity-50"
          >
            {loadingDags ? 'Actualizando…' : 'Actualizar'}
          </button>
        </div>

        {dagsError ? (
          <p className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">{dagsError}</p>
        ) : loadingDags ? (
          <div className="space-y-2">
            {[1, 2].map((n) => (
              <div key={n} className="h-14 animate-pulse rounded-xl bg-slate-100" />
            ))}
          </div>
        ) : dags && dags.total === 0 ? (
          <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 px-6 py-10 text-center">
            <p className="text-sm font-medium text-slate-500">No hay DAGs registrados aún.</p>
            <p className="mt-1 text-xs text-slate-400">
              Crea archivos <code className="rounded bg-slate-100 px-1 py-0.5">*.py</code> en{' '}
              <code className="rounded bg-slate-100 px-1 py-0.5">airflow/dags/</code> y haz git push.
            </p>
          </div>
        ) : dags ? (
          <div className="overflow-hidden rounded-2xl border border-slate-200">
            <table className="w-full text-sm">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                    DAG ID
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Estado
                  </th>
                  <th className="hidden px-4 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500 sm:table-cell">
                    Próxima ejecución
                  </th>
                  <th className="px-4 py-3 text-right text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Acción
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {dags.dags.map((dag) => {
                  const state = triggerState[dag.dag_id] ?? 'idle'
                  const isLoading = state === 'loading'
                  const result = typeof state === 'object' ? state : null

                  return (
                    <tr key={dag.dag_id} className="hover:bg-slate-50">
                      <td className="px-4 py-3 font-medium text-slate-800">{dag.dag_id}</td>
                      <td className="px-4 py-3">
                        <StatusBadge ok={dag.is_active && !dag.is_paused} label={dag.is_paused ? 'Pausado' : dag.is_active ? 'Activo' : 'Inactivo'} />
                      </td>
                      <td className="hidden px-4 py-3 text-slate-500 sm:table-cell">
                        {dag.next_dagrun
                          ? new Date(dag.next_dagrun).toLocaleString('es-CO')
                          : '—'}
                      </td>
                      <td className="px-4 py-3 text-right">
                        {result ? (
                          <span
                            className={`text-xs font-medium ${
                              result.state.startsWith('Error') ? 'text-red-600' : 'text-emerald-600'
                            }`}
                          >
                            {result.state.startsWith('Error') ? result.state : `✓ ${result.state}`}
                          </span>
                        ) : (
                          <button
                            type="button"
                            onClick={() => handleTrigger(dag.dag_id)}
                            disabled={isLoading || dag.is_paused}
                            className="rounded-lg bg-blue-600 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-blue-700 disabled:opacity-50"
                          >
                            {isLoading ? 'Lanzando…' : 'Ejecutar'}
                          </button>
                        )}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        ) : null}
      </div>
    </section>
  )
}
