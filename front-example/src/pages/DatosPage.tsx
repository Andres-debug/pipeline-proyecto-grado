import { useMemo, useState } from 'react'
import type { ChangeEvent } from 'react'
import { usePortalStore } from '../store/usePortalStore'

type PipelineRunResponse = {
  status: string
  message: string
  rows_consolidated: number
  dimensions: Record<string, number>
  kpis_total: number
  warnings: string[]
}

type StepState = 'idle' | 'running' | 'done' | 'error'

const PIPELINE_STEPS = [
  {
    key: 'ingesta',
    label: 'Bronze — Ingesta',
    desc: 'Leyendo y validando el archivo cargado',
    color: 'amber',
  },
  {
    key: 'limpieza',
    label: 'Silver — Limpieza',
    desc: 'Estandarizando columnas, nulos y tipos de datos',
    color: 'sky',
  },
  {
    key: 'modelado',
    label: 'Gold — Star Schema',
    desc: 'Construyendo dimensiones y tabla de hechos',
    color: 'violet',
  },
  {
    key: 'carga',
    label: 'PostgreSQL — Carga',
    desc: 'Persistiendo datos en Aiven Cloud',
    color: 'emerald',
  },
]

const stepColors: Record<string, { ring: string; bg: string; text: string; dot: string }> = {
  amber:   { ring: 'ring-amber-300',   bg: 'bg-amber-50',   text: 'text-amber-700',   dot: 'bg-amber-400' },
  sky:     { ring: 'ring-sky-300',     bg: 'bg-sky-50',     text: 'text-sky-700',     dot: 'bg-sky-400' },
  violet:  { ring: 'ring-violet-300',  bg: 'bg-violet-50',  text: 'text-violet-700',  dot: 'bg-violet-400' },
  emerald: { ring: 'ring-emerald-300', bg: 'bg-emerald-50', text: 'text-emerald-700', dot: 'bg-emerald-400' },
}

function StepIcon({ state, color }: { state: StepState; color: string }) {
  const c = stepColors[color]
  if (state === 'running') {
    return (
      <span className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ring-2 ${c.ring} ${c.bg}`}>
        <svg className={`h-4 w-4 animate-spin ${c.text}`} viewBox="0 0 24 24" fill="none">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3V0a12 12 0 00-12 12h4z" />
        </svg>
      </span>
    )
  }
  if (state === 'done') {
    return (
      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-100 ring-2 ring-emerald-300">
        <svg className="h-4 w-4 text-emerald-600" viewBox="0 0 24 24" fill="currentColor">
          <path fillRule="evenodd" d="M20.707 5.293a1 1 0 010 1.414l-11 11a1 1 0 01-1.414 0l-5-5a1 1 0 111.414-1.414L9 15.586 19.293 5.293a1 1 0 011.414 0z" clipRule="evenodd" />
        </svg>
      </span>
    )
  }
  if (state === 'error') {
    return (
      <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-red-100 ring-2 ring-red-300">
        <svg className="h-4 w-4 text-red-600" viewBox="0 0 24 24" fill="currentColor">
          <path fillRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm-1 5h2v6h-2V7zm0 8h2v2h-2v-2z" clipRule="evenodd" />
        </svg>
      </span>
    )
  }
  return (
    <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-slate-100 ring-2 ring-slate-200">
      <span className={`h-2 w-2 rounded-full ${stepColors[color].dot} opacity-40`} />
    </span>
  )
}

export function DatosPage() {
  const registerUpload = usePortalStore((state) => state.registerUpload)
  const lastUploadedFile = usePortalStore((state) => state.lastUploadedFile)
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null)
  const [selectedFilesCount, setSelectedFilesCount] = useState(0)
  const [isUploading, setIsUploading] = useState(false)
  const [currentStep, setCurrentStep] = useState<number>(-1)
  const [stepStates, setStepStates] = useState<StepState[]>(['idle', 'idle', 'idle', 'idle'])
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [runSummary, setRunSummary] = useState<PipelineRunResponse | null>(null)

  const uploadDate = useMemo(() => {
    if (!lastUploadedFile) return null
    return new Date(lastUploadedFile.uploadedAt).toLocaleString('es-CO')
  }, [lastUploadedFile])

  const setStep = (index: number, state: StepState) => {
    setCurrentStep(index)
    setStepStates((prev) => {
      const next = [...prev]
      next[index] = state
      return next
    })
  }

  const resetSteps = () => {
    setCurrentStep(-1)
    setStepStates(['idle', 'idle', 'idle', 'idle'])
  }

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files ?? [])
    if (files.length === 0) return

    const supportedTypes = ['.csv', '.xlsx', '.xls']
    const invalidFile = files.find((f) => {
      const ext = f.name.slice(f.name.lastIndexOf('.')).toLowerCase()
      return !supportedTypes.includes(ext)
    })
    if (invalidFile) {
      setErrorMessage(`Formato no soportado: ${invalidFile.name}. Usa CSV, XLS o XLSX.`)
      setRunSummary(null)
      return
    }

    setIsUploading(true)
    setErrorMessage(null)
    setRunSummary(null)
    resetSteps()

    // Simular progreso visible de los primeros 3 pasos mientras la API procesa
    setStep(0, 'running')
    await new Promise((r) => setTimeout(r, 700))
    setStep(0, 'done')
    setStep(1, 'running')
    await new Promise((r) => setTimeout(r, 800))
    setStep(1, 'done')
    setStep(2, 'running')

    const formData = new FormData()
    files.forEach((f) => formData.append('files', f))

    try {
      const response = await fetch('/api/pipeline/upload-run', {
        method: 'POST',
        body: formData,
      })
      const data = (await response.json()) as PipelineRunResponse | { detail?: string }

      if (!response.ok) {
        const detail = typeof data === 'object' && data && 'detail' in data ? data.detail : null
        setStep(2, 'error')
        throw new Error(detail ?? 'No se pudo procesar el archivo en el pipeline.')
      }

      setStep(2, 'done')
      setStep(3, 'running')
      await new Promise((r) => setTimeout(r, 400))
      setStep(3, 'done')

      registerUpload(files[0])
      setSelectedFileName(files[0].name)
      setSelectedFilesCount(files.length)
      setRunSummary(data as PipelineRunResponse)
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'Error inesperado durante la carga.')
      setStepStates((prev) => prev.map((s) => (s === 'running' ? 'error' : s)))
    } finally {
      setIsUploading(false)
      setCurrentStep(-1)
      event.target.value = ''
    }
  }

  const allDone = stepStates.every((s) => s === 'done')

  return (
    <div className="space-y-6">
      <div className="grid gap-5 lg:grid-cols-3">

        {/* Upload zone */}
        <div className="lg:col-span-2 space-y-4">
          <label
            htmlFor="data-file"
            className={`group relative flex cursor-pointer flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed p-10 text-center transition-all duration-200 ${
              isUploading
                ? 'cursor-wait border-blue-300 bg-blue-50/60'
                : 'border-slate-200 bg-slate-50/50 hover:border-blue-400 hover:bg-blue-50/40'
            }`}
          >
            <input
              id="data-file"
              type="file"
              accept=".csv,.xls,.xlsx"
              multiple
              className="sr-only"
              onChange={handleFileChange}
              disabled={isUploading}
            />

            <div className={`flex h-14 w-14 items-center justify-center rounded-2xl transition-colors ${isUploading ? 'bg-blue-100' : 'bg-white shadow-sm group-hover:bg-blue-50'}`}>
              {isUploading ? (
                <svg className="h-7 w-7 animate-spin text-blue-600" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3V0a12 12 0 00-12 12h4z" />
                </svg>
              ) : (
                <svg className="h-7 w-7 text-blue-500 group-hover:text-blue-600" viewBox="0 0 24 24" fill="none">
                  <path d="M21 15V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                  <path d="M12 3V15M12 3L8 7M12 3L16 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              )}
            </div>

            <div>
              <p className="text-base font-semibold text-slate-700">
                {isUploading
                  ? 'Ejecutando pipeline ETL…'
                  : allDone
                  ? '¡Pipeline completado!'
                  : 'Arrastra tu archivo aquí'}
              </p>
              <p className="mt-1 text-sm text-slate-500">
                {isUploading
                  ? `Procesando: ${selectedFileName ?? 'archivo'}`
                  : selectedFileName
                  ? `${selectedFileName}${selectedFilesCount > 1 ? ` (+${selectedFilesCount - 1} más)` : ''}`
                  : 'o haz clic para seleccionar — CSV, XLS, XLSX'}
              </p>
            </div>

            {!isUploading && !allDone && (
              <span className="rounded-xl bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white shadow-sm transition group-hover:bg-blue-700">
                Seleccionar archivo
              </span>
            )}
            {allDone && !isUploading && (
              <span className="rounded-xl bg-emerald-600 px-6 py-2.5 text-sm font-semibold text-white shadow-sm">
                Subir otro archivo
              </span>
            )}
          </label>

          {errorMessage && (
            <div className="flex items-start gap-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3">
              <svg className="mt-0.5 h-4 w-4 shrink-0 text-rose-500" viewBox="0 0 24 24" fill="currentColor">
                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm-1 5h2v6h-2V7zm0 8h2v2h-2v-2z" clipRule="evenodd" />
              </svg>
              <p className="text-sm text-rose-700">{errorMessage}</p>
            </div>
          )}
        </div>

        {/* Pipeline steps panel */}
        <div className="flex flex-col gap-3">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="mb-4 text-xs font-semibold uppercase tracking-widest text-slate-400">
              Proceso ETL
            </p>
            <div className="space-y-3">
              {PIPELINE_STEPS.map((step, i) => {
                const state = stepStates[i]
                const c = stepColors[step.color]
                const isActive = state === 'running'
                return (
                  <div
                    key={step.key}
                    className={`flex items-start gap-3 rounded-xl p-3 transition-all duration-300 ${
                      isActive ? `${c.bg} ring-1 ${c.ring}` : state === 'done' ? 'bg-emerald-50/60' : 'bg-slate-50'
                    }`}
                  >
                    <StepIcon state={state} color={step.color} />
                    <div className="min-w-0">
                      <p className={`text-sm font-semibold transition-colors ${
                        isActive ? c.text : state === 'done' ? 'text-emerald-700' : 'text-slate-500'
                      }`}>
                        {step.label}
                      </p>
                      <p className="mt-0.5 text-xs text-slate-400 leading-tight">{step.desc}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Status */}
          <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
            <div className="flex items-center gap-2">
              <span className={`h-2 w-2 rounded-full transition-colors ${
                isUploading ? 'animate-pulse bg-blue-500' : allDone ? 'bg-emerald-500' : 'bg-slate-300'
              }`} />
              <p className="text-xs font-medium text-slate-600">
                {isUploading
                  ? `Paso ${currentStep + 1} de ${PIPELINE_STEPS.length}`
                  : allDone
                  ? 'Pipeline completado'
                  : lastUploadedFile
                  ? `Última carga: ${uploadDate}`
                  : 'Esperando archivo'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Results */}
      {runSummary && (
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50/60 p-5">
          <div className="mb-4 flex items-center gap-2">
            <svg className="h-5 w-5 text-emerald-600" viewBox="0 0 24 24" fill="currentColor">
              <path fillRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm4.707 7.293a1 1 0 00-1.414 0L10 14.586l-2.293-2.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l6-6a1 1 0 000-1.414z" clipRule="evenodd" />
            </svg>
            <p className="font-semibold text-emerald-800">Pipeline ejecutado correctamente</p>
          </div>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              { label: 'Registros consolidados', value: runSummary.rows_consolidated.toLocaleString() },
              { label: 'KPIs generados', value: runSummary.kpis_total },
              { label: 'Dimensiones', value: Object.keys(runSummary.dimensions).length },
              { label: 'Advertencias', value: runSummary.warnings.length },
            ].map(({ label, value }) => (
              <div key={label} className="rounded-xl bg-white p-4 shadow-sm">
                <p className="text-2xl font-bold text-slate-800">{value}</p>
                <p className="mt-1 text-xs text-slate-500">{label}</p>
              </div>
            ))}
          </div>
          {Object.keys(runSummary.dimensions).length > 0 && (
            <div className="mt-4 flex flex-wrap gap-2">
              {Object.entries(runSummary.dimensions).map(([key, value]) => (
                <span key={key} className="rounded-lg bg-white px-3 py-1.5 text-xs font-medium text-slate-700 shadow-sm ring-1 ring-slate-200">
                  {key}: <span className="font-bold text-blue-700">{value}</span>
                </span>
              ))}
            </div>
          )}
          {runSummary.warnings.length > 0 && (
            <p className="mt-3 text-xs text-emerald-700 opacity-70">{runSummary.warnings.join(' · ')}</p>
          )}
        </div>
      )}
    </div>
  )
}
