import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import { SidebarMenu } from '../components/SidebarMenu'
import { usePortalStore } from '../store/usePortalStore'

const sectionTitles: Record<string, string> = {
  '/dashboard': 'Dashboard de Analitica',
  '/datos': 'Carga y Procesamiento de Datos',
  '/perfil': 'Perfil de Administrador',
}

export function PortalLayout() {
  const currentUser = usePortalStore((state) => state.currentUser)
  const logout = usePortalStore((state) => state.logout)
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }

  const title = sectionTitles[location.pathname] ?? 'Portal Institucional'

  if (!currentUser) {
    return null
  }

  return (
    <main className="min-h-screen bg-slate-100 p-2 sm:p-3 md:p-6">
      <section className="mx-auto flex min-h-[calc(100vh-1rem)] w-full max-w-7xl overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-xl md:min-h-[calc(100vh-3rem)]">
        <SidebarMenu onLogout={handleLogout} universityName={currentUser.universityName} />

        <div className="min-w-0 flex-1 p-4 sm:p-5 md:p-8">
          <header className="border-b border-slate-200 pb-5">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-700">Universidad conectada</p>
            <h2 className="mt-2 text-xl font-bold text-slate-800 sm:text-2xl md:text-3xl">{title}</h2>
            <p className="mt-1 text-sm text-slate-600">{currentUser.email}</p>
          </header>

          <div className="mt-6">
            <Outlet />
          </div>
        </div>
      </section>
    </main>
  )
}
