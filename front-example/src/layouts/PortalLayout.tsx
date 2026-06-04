import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import { SidebarMenu } from '../components/SidebarMenu'
import { usePortalStore } from '../store/usePortalStore'

const sectionMeta: Record<string, { title: string; subtitle: string }> = {
  '/admin': {
    title: 'Panel de Administración',
    subtitle: 'Gestión del pipeline y monitoreo de Airflow',
  },
  '/dashboard': {
    title: 'Dashboard de Analítica',
    subtitle: 'Indicadores consolidados de movilidad académica',
  },
  '/datos': {
    title: 'Carga y Procesamiento',
    subtitle: 'Sube archivos CSV/XLSX para ejecutar el pipeline ETL',
  },
  '/perfil': {
    title: 'Perfil de Usuario',
    subtitle: 'Información de tu cuenta institucional',
  },
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

  const meta = sectionMeta[location.pathname] ?? { title: 'Portal Institucional', subtitle: '' }

  if (!currentUser) return null

  return (
    <div className="min-h-screen bg-slate-100" style={{ backgroundImage: 'radial-gradient(circle at 20% 50%, #dbeafe22 0%, transparent 60%), radial-gradient(circle at 80% 20%, #e0e7ff22 0%, transparent 50%)' }}>
      <div className="mx-auto flex min-h-screen max-w-[1440px] p-2 sm:p-3 md:p-5">
        <div className="flex w-full overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl shadow-slate-200/80 md:rounded-3xl">

          <SidebarMenu
            onLogout={handleLogout}
            universityName={currentUser.universityName}
            role={currentUser.role}
          />

          <div className="flex min-w-0 flex-1 flex-col">
            {/* Header */}
            <header className="border-b border-slate-100 bg-white px-5 py-4 md:px-8 md:py-5">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-[11px] font-semibold uppercase tracking-widest text-blue-600">
                    Universidad conectada
                  </p>
                  <h1 className="mt-1 text-xl font-bold text-slate-900 sm:text-2xl">
                    {meta.title}
                  </h1>
                  <p className="mt-0.5 text-sm text-slate-500">{meta.subtitle}</p>
                </div>
                <div className="hidden shrink-0 items-center gap-2 md:flex">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-50 text-xs font-bold text-blue-700">
                    {currentUser.email.charAt(0).toUpperCase()}
                  </div>
                  <div className="text-right">
                    <p className="text-xs font-semibold text-slate-700">{currentUser.email}</p>
                    <p className="text-[11px] text-slate-400 capitalize">{currentUser.role}</p>
                  </div>
                </div>
              </div>
            </header>

            {/* Content */}
            <main className="flex-1 overflow-auto p-4 sm:p-5 md:p-8">
              <div key={location.pathname} className="page-transition">
                <Outlet />
              </div>
            </main>
          </div>
        </div>
      </div>
    </div>
  )
}
