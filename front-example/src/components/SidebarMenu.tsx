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
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5" aria-hidden="true">
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
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5" aria-hidden="true">
        <path d="M4 4H10V10H4V4ZM14 4H20V10H14V4ZM4 14H10V20H4V14ZM14 14H20V20H14V14Z" stroke="currentColor" strokeWidth="1.8" />
      </svg>
    ),
  },
  {
    label: 'Datos',
    to: '/datos',
    roles: ['admin', 'user'],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5" aria-hidden="true">
        <path d="M5 4H19V20H5V4Z" stroke="currentColor" strokeWidth="1.8" />
        <path d="M8 9H16M8 13H16M8 17H13" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    label: 'Perfil',
    to: '/perfil',
    roles: ['admin', 'user'],
    icon: (
      <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5" aria-hidden="true">
        <path d="M12 12C14.4853 12 16.5 9.98528 16.5 7.5C16.5 5.01472 14.4853 3 12 3C9.51472 3 7.5 5.01472 7.5 7.5C7.5 9.98528 9.51472 12 12 12Z" stroke="currentColor" strokeWidth="1.8" />
        <path d="M4 20C4 16.6863 7.58172 14 12 14C16.4183 14 20 16.6863 20 20" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
      </svg>
    ),
  },
]

export function SidebarMenu({ onLogout, universityName, role }: SidebarMenuProps) {
  const visibleItems = menuItems.filter((item) => item.roles.includes(role))

  return (
    <aside className="flex w-[84px] shrink-0 flex-col bg-[#0b1022] p-3 text-slate-100 md:w-[280px] md:p-5">
      <div>
        <p className="hidden text-xs font-semibold uppercase tracking-[0.2em] text-blue-200 md:block">TravelUniData</p>
        <p className="text-center text-lg font-bold text-blue-100 md:hidden">TU</p>
        <h1 className="mt-2 hidden text-lg font-bold text-white md:block">Panel Institucional</h1>
        <p className="mt-1 hidden text-xs text-slate-400 md:block">{universityName}</p>
        {role === 'admin' && (
          <span className="mt-2 hidden rounded-full bg-blue-600/30 px-2 py-0.5 text-xs font-semibold text-blue-300 md:inline-block">
            Administrador
          </span>
        )}
      </div>

      <nav className="mt-5 space-y-2 md:mt-8">
        {visibleItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center justify-center rounded-xl px-3 py-3 text-sm font-medium transition md:justify-start md:gap-3 md:px-4 ${
                isActive
                  ? 'bg-white text-[#0b1022] shadow-sm'
                  : 'text-slate-300 hover:bg-white/10 hover:text-white'
              }`
            }
            aria-label={item.label}
          >
            {item.icon}
            <span className="hidden md:inline">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <button
        type="button"
        onClick={onLogout}
        className="mt-auto flex items-center justify-center rounded-xl border border-white/20 px-3 py-3 text-sm font-semibold text-slate-200 transition hover:bg-white/10 md:justify-start md:gap-3 md:px-4"
        aria-label="Cerrar Sesion"
      >
        <svg viewBox="0 0 24 24" fill="none" className="h-5 w-5" aria-hidden="true">
          <path d="M15 17L20 12L15 7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M20 12H9" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
          <path d="M11 4H6C4.89543 4 4 4.89543 4 6V18C4 19.1046 4.89543 20 6 20H11" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        </svg>
        <span className="hidden md:inline">Cerrar Sesion</span>
      </button>
    </aside>
  )
}
