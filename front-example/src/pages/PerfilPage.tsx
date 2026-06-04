import { usePortalStore } from '../store/usePortalStore'

export function PerfilPage() {
  const currentUser = usePortalStore((state) => state.currentUser)

  if (!currentUser) return null

  const initials = currentUser.email.slice(0, 2).toUpperCase()

  return (
    <div className="space-y-5 max-w-2xl">
      {/* Avatar card */}
      <div className="flex items-center gap-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl bg-blue-600 text-xl font-bold text-white shadow-md shadow-blue-200">
          {initials}
        </div>
        <div>
          <p className="text-lg font-bold text-slate-900">{currentUser.universityName}</p>
          <p className="text-sm text-slate-500">{currentUser.email}</p>
          <span className="mt-2 inline-flex items-center gap-1.5 rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-semibold text-blue-700">
            <span className="h-1.5 w-1.5 rounded-full bg-blue-500" />
            Administrador institucional
          </span>
        </div>
      </div>

      {/* Info cards */}
      <div className="grid gap-4 sm:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="mb-3 text-xs font-semibold uppercase tracking-widest text-blue-600">Acceso</p>
          <div className="space-y-2.5">
            {[
              { label: 'Universidad', value: currentUser.universityName },
              { label: 'Correo', value: currentUser.email },
              { label: 'Rol', value: 'Administrador institucional' },
            ].map(({ label, value }) => (
              <div key={label}>
                <p className="text-[11px] font-medium uppercase tracking-wide text-slate-400">{label}</p>
                <p className="text-sm font-medium text-slate-800">{value}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-2xl border border-slate-100 bg-slate-50 p-5">
          <p className="mb-3 text-xs font-semibold uppercase tracking-widest text-slate-400">Permisos</p>
          <div className="space-y-2">
            {[
              'Carga y procesamiento de datos',
              'Panel de administración del pipeline',
              'Monitoreo de DAGs en Airflow',
              'Visualización del dashboard BI',
            ].map((perm) => (
              <div key={perm} className="flex items-center gap-2">
                <svg className="h-4 w-4 shrink-0 text-emerald-500" viewBox="0 0 24 24" fill="currentColor">
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm4.707 7.293a1 1 0 00-1.414 0L10 14.586l-2.293-2.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l6-6a1 1 0 000-1.414z" clipRule="evenodd" />
                </svg>
                <p className="text-xs text-slate-600">{perm}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
