import type { ReactNode } from 'react'
import { NavLink } from 'react-router-dom'
import type { UserRole } from '../store/usePortalStore'

type SidebarMenuProps = {
  onLogout: () => void
  universityName: string
  role: UserRole
}

type MenuItem = {
  label: string
  to: '/dashboard' | '/datos' | '/perfil' | '/admin'
  icon: ReactNode
  roles: UserRole[]
}

const menuItems: MenuItem[] = [
  {
    label: 'Admin Pipeline',
    to: '/admin',
    roles: ['admin'],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5 shrink-0" aria-hidden="true">
        <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
        <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
        <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    label: 'Dashboard',
    to: '/dashboard',
    roles: ['admin', 'user'],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5 shrink-0" aria-hidden="true">
        <rect x="3" y="3" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.8" />
        <rect x="14" y="3" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.8" />
        <rect x="3" y="14" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.8" />
        <rect x="14" y="14" width="7" height="7" rx="1.5" stroke="currentColor" strokeWidth="1.8" />
      </svg>
    ),
  },
  {
    label: 'Datos',
    to: '/datos',
    roles: ['admin', 'user'],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5 shrink-0" aria-hidden="true">
        <path d="M21 15V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V15" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        <path d="M12 3V15M12 3L8 7M12 3L16 7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    label: 'Perfil',
    to: '/perfil',
    roles: ['admin', 'user'],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5 shrink-0" aria-hidden="true">
        <circle cx="12" cy="8" r="4" stroke="currentColor" strokeWidth="1.8" />
        <path d="M4 20C4 16.6863 7.58172 14 12 14C16.4183 14 20 16.6863 20 20" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      </svg>
    ),
  },
]

export function SidebarMenu({ onLogout, universityName, role }: SidebarMenuProps) {
  const visibleItems = menuItems.filter((item) => item.roles.includes(role))

  return (
    <aside
      className="flex w-[72px] shrink-0 flex-col md:w-[256px]"
      style={{ background: 'linear-gradient(180deg, #0f172a 0%, #1a2744 100%)' }}
    >
      {/* Brand */}
      <div className="border-b border-white/10 px-3 py-5 md:px-5 md:py-6">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-600 shadow-lg shadow-blue-900/40">
            <span className="text-xs font-bold tracking-tight text-white">TU</span>
          </div>
          <div className="hidden md:block min-w-0">
            <p className="text-[10px] font-semibold uppercase tracking-widest text-blue-400">TravelUniData</p>
            <p className="mt-0.5 truncate text-sm font-bold text-white">Panel Institucional</p>
          </div>
        </div>
        {role === 'admin' && (
          <div className="mt-3 hidden md:flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
            <span className="text-[11px] font-medium text-slate-400">Administrador</span>
          </div>
        )}
      </div>

      {/* Nav */}
      <nav className="flex-1 space-y-0.5 p-2.5 md:p-3">
        {visibleItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            aria-label={item.label}
            className={({ isActive }) =>
              `group flex items-center justify-center rounded-xl px-2.5 py-2.5 text-sm font-medium transition-all duration-150 md:justify-start md:gap-3 md:px-3 ${
                isActive
                  ? 'bg-white text-slate-900 shadow-md'
                  : 'text-slate-400 hover:bg-white/8 hover:text-white'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <span className={isActive ? 'text-blue-600' : ''}>{item.icon}</span>
                <span className="hidden md:inline">{item.label}</span>
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="border-t border-white/10 p-2.5 md:p-3">
        <div className="mb-2 hidden rounded-xl bg-white/5 px-3 py-2.5 md:block">
          <p className="truncate text-xs font-semibold text-slate-200">{universityName}</p>
          <p className="mt-0.5 text-[11px] text-slate-500">Institución conectada</p>
        </div>
        <button
          type="button"
          onClick={onLogout}
          aria-label="Cerrar Sesion"
          className="flex w-full items-center justify-center gap-2.5 rounded-xl border border-white/10 px-2.5 py-2.5 text-sm font-medium text-slate-400 transition-all duration-150 hover:border-rose-500/40 hover:bg-rose-500/10 hover:text-rose-300 md:justify-start md:px-3"
        >
          <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5 shrink-0" aria-hidden="true">
            <path d="M15 17L20 12L15 7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M20 12H9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
            <path d="M11 4H6C4.89543 4 4 4.89543 4 6V18C4 19.1046 4.89543 20 6 20H11" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
          </svg>
          <span className="hidden md:inline">Cerrar Sesión</span>
        </button>
      </div>
    </aside>
  )
}
