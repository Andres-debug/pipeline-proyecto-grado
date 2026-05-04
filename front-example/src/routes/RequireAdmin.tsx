import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { usePortalStore } from '../store/usePortalStore'

export function RequireAdmin() {
  const currentUser = usePortalStore((state) => state.currentUser)
  const location = useLocation()

  if (!currentUser) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  if (currentUser.role !== 'admin') {
    return <Navigate to="/dashboard" replace />
  }

  return <Outlet />
}
