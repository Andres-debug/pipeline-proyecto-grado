import { usePortalStore } from '../store/usePortalStore'

export function PerfilPage() {
  const currentUser = usePortalStore((state) => state.currentUser)

  if (!currentUser) {
    return null
  }

  return (
    <section className="grid gap-5 md:grid-cols-2">
      <div className="rounded-2xl border border-slate-200 bg-white p-5">
        <p className="text-xs font-semibold uppercase tracking-wide text-blue-700">Usuario</p>
        <p className="mt-3 text-sm text-slate-700">Universidad: {currentUser.universityName}</p>
        <p className="text-sm text-slate-700">Correo: {currentUser.email}</p>
        <p className="text-sm text-slate-700">Rol: Administrador institucional</p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
        <p className="text-xs font-semibold uppercase tracking-wide text-blue-700">Resumen</p>
        <p className="mt-3 text-sm text-slate-700">
          Este perfil permite gestionar la carga de datos y consultar los resultados analiticos del pipeline.
        </p>
      </div>
    </section>
  )
}
