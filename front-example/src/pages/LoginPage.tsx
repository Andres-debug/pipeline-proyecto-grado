import { useState } from 'react'
import type { FormEvent } from 'react'
import { Navigate } from 'react-router-dom'
import loginImg from '../assets/login.jpg'
import { usePortalStore } from '../store/usePortalStore'

export function LoginPage() {
  const { currentUser, login, loginError, clearLoginError } = usePortalStore()
  const [email, setEmail] = useState('admin@travelunidata.edu.co')
  const [password, setPassword] = useState('admin2024')

  const handleLogin = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    login(email.trim(), password)
  }

  if (currentUser) return <Navigate to="/dashboard" replace />

  return (
    <main className="min-h-screen" style={{ background: 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%)' }}>
      <div className="grid min-h-screen grid-cols-1 md:grid-cols-2">

        {/* Left — image */}
        <div className="hidden items-center justify-center p-10 md:flex">
          <div className="relative w-full max-w-lg">
            <div className="absolute -inset-4 rounded-3xl bg-blue-500/10 blur-2xl" />
            <img
              src={loginImg}
              alt="Portal institucional"
              className="relative w-full rounded-3xl object-cover shadow-2xl"
              style={{ height: '520px' }}
            />
            <div className="absolute bottom-6 left-6 right-6 rounded-2xl bg-black/40 p-4 backdrop-blur-sm">
              <p className="text-sm font-semibold text-white">TravelUniData</p>
              <p className="mt-0.5 text-xs text-blue-200">Plataforma de analítica de movilidad académica</p>
            </div>
          </div>
        </div>

        {/* Right — form */}
        <div className="flex items-center justify-center p-6 md:p-10">
          <div className="w-full max-w-md">
            {/* Logo */}
            <div className="mb-8 flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 shadow-lg shadow-blue-900/50">
                <span className="text-sm font-bold text-white">TU</span>
              </div>
              <div>
                <p className="text-[11px] font-semibold uppercase tracking-widest text-blue-400">TravelUniData</p>
                <p className="text-sm font-bold text-white">Panel Institucional</p>
              </div>
            </div>

            {/* Card */}
            <div className="rounded-3xl bg-white p-8 shadow-2xl">
              <h2 className="text-2xl font-bold text-slate-900">Bienvenido</h2>
              <p className="mt-1.5 text-sm text-slate-500">
                Inicia sesión para gestionar los datos de tu universidad
              </p>

              <form className="mt-7 space-y-4" onSubmit={handleLogin}>
                <div className="space-y-1">
                  <label htmlFor="email" className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Correo institucional
                  </label>
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => { setEmail(e.target.value); clearLoginError() }}
                    placeholder="usuario@universidad.edu.co"
                    className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100"
                    required
                  />
                </div>

                <div className="space-y-1">
                  <label htmlFor="password" className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Contraseña
                  </label>
                  <input
                    id="password"
                    type="password"
                    value={password}
                    onChange={(e) => { setPassword(e.target.value); clearLoginError() }}
                    placeholder="••••••••"
                    className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100"
                    required
                  />
                </div>

                {loginError && (
                  <div className="flex items-center gap-2 rounded-xl border border-red-200 bg-red-50 px-3 py-2.5">
                    <svg className="h-4 w-4 shrink-0 text-red-500" viewBox="0 0 24 24" fill="currentColor">
                      <path fillRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm-1 5h2v6h-2V7zm0 8h2v2h-2v-2z" clipRule="evenodd" />
                    </svg>
                    <p className="text-sm text-red-700">{loginError}</p>
                  </div>
                )}

                <button
                  type="submit"
                  className="w-full rounded-xl bg-blue-600 py-3 text-sm font-semibold text-white shadow-md shadow-blue-200 transition hover:bg-blue-700 active:scale-[0.98]"
                >
                  Ingresar al portal
                </button>

                <p className="text-center text-xs text-slate-400 hover:text-slate-600 cursor-pointer transition">
                  ¿Olvidaste tu contraseña?
                </p>
              </form>

              {/* Demo credentials */}
              <div className="mt-5 rounded-xl border border-slate-100 bg-slate-50 p-4">
                <p className="mb-2 text-xs font-semibold text-slate-600">Credenciales demo</p>
                <div className="space-y-1.5">
                  <div>
                    <span className="inline-block rounded-full bg-blue-100 px-2 py-0.5 text-[10px] font-bold text-blue-700">Admin</span>
                    <p className="mt-0.5 text-xs text-slate-500">admin@travelunidata.edu.co / admin2024</p>
                  </div>
                  <div>
                    <span className="inline-block rounded-full bg-slate-200 px-2 py-0.5 text-[10px] font-bold text-slate-600">Usuario</span>
                    <p className="mt-0.5 text-xs text-slate-500">universidad@demo.edu.co / demo123</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
