import { useMemo, useState } from 'react'
import type { ChangeEvent, FormEvent } from 'react'
import { usePortalStore } from './store/usePortalStore'
import loginImg from './assets/login.jpg'

function App() {
  const { currentUser, login, logout, loginError, clearLoginError, registerUpload, lastUploadedFile } =
    usePortalStore()

  const [email, setEmail] = useState('admin@universidada.edu.co')
  const [password, setPassword] = useState('demo123')
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null)

  const uploadDate = useMemo(() => {
    if (!lastUploadedFile) {
      return null
    }
    return new Date(lastUploadedFile.uploadedAt).toLocaleString('es-CO')
  }, [lastUploadedFile])

  const handleLogin = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    login(email.trim(), password)
  }

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) {
      return
    }
    registerUpload(file)
    setSelectedFileName(file.name)
  }

  if (!currentUser) {
    return (
      <main className="min-h-screen bg-[#ececec]">
        <section className="grid min-h-screen grid-cols-1 md:grid-cols-2">
          <div className="relative flex items-center justify-center p-4 md:p-8">
            <div className="h-full w-full max-w-2xl">
              <img
                src={loginImg}
                alt="Ilustración de acceso al portal"
                className="mx-auto h-[360px] w-full rounded-3xl object-cover shadow-sm md:h-[560px]"
              />
            </div>
          </div>

          <div className="relative flex items-center justify-center overflow-hidden rounded-l-[2.5rem] bg-[#1877d7] p-6 md:p-10">
            <div className="relative z-10 w-full max-w-md rounded-2xl bg-[#f3f3f3] p-7 shadow-xl">
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[#1877d7]">TravelUniData</p>
              <h2 className="text-3xl font-bold text-slate-800">Bienvenido</h2>
              <p className="mt-3 text-base text-slate-600">Inicia sesión para gestionar los datos de tu universidad</p>

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
                  placeholder="Contraseña"
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

                <p className="text-sm text-slate-500">¿Olvidaste tu contraseña?</p>
              </form>

              <div className="mt-4 rounded-xl bg-white px-4 py-3 text-xs text-slate-600">
                <p className="font-semibold text-slate-700">Credenciales demo</p>
                <p className="mt-1">admin@universidada.edu.co / demo123</p>
                <p>admin@universidadb.edu.co / demo123</p>
                <p>admin@universidadc.edu.co / demo123</p>
              </div>
            </div>

            <div className="pointer-events-none absolute -bottom-16 -right-14 h-80 w-80 rounded-full border border-white/60" />
            <div className="pointer-events-none absolute -bottom-28 -right-28 h-96 w-96 rounded-full border border-white/50" />
          </div>
        </section>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 to-blue-50 px-4 py-8 md:px-8 md:py-10">
      <section className="mx-auto w-full max-w-5xl rounded-3xl border border-blue-100 bg-white p-6 shadow-xl md:p-8">
        <div className="flex flex-col gap-4 border-b border-blue-100 pb-6 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-blue-700">Universidad conectada</p>
            <h1 className="text-2xl font-bold text-slate-800 md:text-3xl">Portal de Carga de Datos</h1>
            <p className="mt-1 text-sm text-slate-600">{currentUser.universityName}</p>
            <p className="text-sm text-slate-500">{currentUser.email}</p>
          </div>

          <button
            type="button"
            onClick={logout}
            className="rounded-xl border border-blue-200 px-4 py-2 text-sm font-medium text-blue-800 transition hover:bg-blue-50"
          >
            Cerrar sesión
          </button>
        </div>

        <div className="mt-8 grid gap-6 md:grid-cols-3">
          <div className="rounded-2xl border border-blue-100 bg-blue-50/70 p-4 md:col-span-2">
            <h2 className="text-lg font-semibold text-slate-800">Subir archivo de Data</h2>
            <p className="mt-1 text-sm text-slate-600">
              Carga aquí los archivos de internacionalización (CSV, XLSX, JSON) para procesarlos en el pipeline.
            </p>

            <label
              htmlFor="data-file"
              className="mt-4 inline-flex cursor-pointer items-center rounded-xl bg-blue-700 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-800"
            >
              Seleccionar archivo
            </label>
            <input id="data-file" type="file" className="hidden" onChange={handleFileChange} />

            <p className="mt-3 text-sm text-slate-700">
              {selectedFileName ? `Archivo seleccionado: ${selectedFileName}` : 'No hay archivo seleccionado'}
            </p>
          </div>

          <div className="rounded-2xl border border-blue-100 bg-white p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-blue-700">Alcance Analítico</p>
            <p className="mt-2 text-sm text-slate-600">
              Esta plataforma consolida información para análisis descriptivos y modelos predictivos institucionales.
            </p>
          </div>
        </div>

        {lastUploadedFile && (
          <div className="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900">
            <p className="font-semibold">Última carga registrada</p>
            <p className="mt-1">Archivo: {lastUploadedFile.name}</p>
            <p>Tamaño: {(lastUploadedFile.size / 1024).toFixed(1)} KB</p>
            <p>Tipo: {lastUploadedFile.type}</p>
            <p>Fecha: {uploadDate}</p>
          </div>
        )}

        <div className="mt-6 rounded-2xl border border-blue-100 bg-blue-50/50 p-4 text-sm text-slate-600">
          <p className="font-semibold">Objetivo del portal</p>
          <p>
            Centralizar la carga de datos de internacionalización y habilitar visualización de indicadores descriptivos
            junto con resultados predictivos para apoyo a la toma de decisiones académicas.
          </p>
        </div>
      </section>
    </main>
  )
}

export default App
