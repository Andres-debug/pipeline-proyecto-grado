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

  if (currentUser) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <main className="min-h-screen bg-[#ececec]">
      <section className="grid min-h-screen grid-cols-1 md:grid-cols-2">
        <div className="relative flex items-center justify-center p-4 md:p-8">
          <div className="h-full w-full max-w-2xl">
            <img
              src={loginImg}
              alt="Ilustracion de acceso al portal"
              className="mx-auto h-[280px] w-full rounded-3xl object-cover shadow-sm sm:h-[360px] md:h-[560px]"
            />
          </div>
        </div>

        <div className="relative flex items-center justify-center overflow-hidden rounded-none bg-[#1877d7] p-6 md:rounded-l-[2.5rem] md:p-10">
          <div className="relative z-10 w-full max-w-md rounded-2xl bg-[#f3f3f3] p-7 shadow-xl">
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#1877d7]">TravelUniData</p>
            <h2 className="text-3xl font-bold text-slate-800">Bienvenido</h2>
            <p className="mt-3 text-base text-slate-600">Inicia sesion para gestionar los datos de tu universidad</p>

            <form className="mt-7 space-y-4" onSubmit={handleLogin}>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) => {
                  setEmail(event.target.value)
                  clearLoginError()
                }}
                placeholder="Correo institucional"
                className="w-full rounded-full border border-slate-300 bg-white px-5 py-3 text-slate-700 outline-none ring-blue-200 focus:border-blue-500 focus:ring"
                required
              />

              <input
                id="password"
                type="password"
                value={password}
                onChange={(event) => {
                  setPassword(event.target.value)
                  clearLoginError()
                }}
                placeholder="Contrasena"
                className="w-full rounded-full border border-slate-300 bg-white px-5 py-3 text-slate-700 outline-none ring-blue-200 focus:border-blue-500 focus:ring"
                required
              />

              {loginError && <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">{loginError}</p>}

              <button
                type="submit"
                className="w-full rounded-full bg-[#1877d7] px-4 py-3 font-semibold text-white transition hover:bg-[#156bc2]"
              >
                Ingresar al portal
              </button>

              <p className="text-sm text-slate-500">Olvidaste tu contrasena?</p>
            </form>

            <div className="mt-4 rounded-xl bg-white px-4 py-3 text-xs text-slate-600">
              <p className="font-semibold text-slate-700">Credenciales demo</p>
              <p className="mt-1 font-medium text-blue-700">Admin (pipeline + Airflow)</p>
              <p>admin@travelunidata.edu.co / admin2024</p>
              <p className="mt-1 font-medium text-slate-600">Usuario (PowerBI + carga)</p>
              <p>universidad@demo.edu.co / demo123</p>
            </div>
          </div>

          <div className="pointer-events-none absolute -bottom-16 -right-14 h-80 w-80 rounded-full border border-white/60" />
          <div className="pointer-events-none absolute -bottom-28 -right-28 h-96 w-96 rounded-full border border-white/50" />
        </div>
      </section>
    </main>
  )
}
