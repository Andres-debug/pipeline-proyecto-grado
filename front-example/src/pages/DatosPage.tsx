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

export function DatosPage() {
  const registerUpload = usePortalStore((state) => state.registerUpload)
  const lastUploadedFile = usePortalStore((state) => state.lastUploadedFile)
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null)
  const [selectedFilesCount, setSelectedFilesCount] = useState(0)
  const [isUploading, setIsUploading] = useState(false)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [runSummary, setRunSummary] = useState<PipelineRunResponse | null>(null)

  const uploadDate = useMemo(() => {
    if (!lastUploadedFile) return null
    return new Date(lastUploadedFile.uploadedAt).toLocaleString('es-CO')
  }, [lastUploadedFile])

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files ?? [])
    if (files.length === 0) return

    const supportedTypes = ['.csv', '.xlsx', '.xls']
    const invalidFile = files.find((f) => {
      const ext = f.name.slice(f.name.lastIndexOf('.')).toLowerCase()
      return !supportedTypes.includes(ext)
    })
    if (invalidFile) {
      setErrorMessage(`Formato no soportado: ${invalidFile.name}. Carga archivos CSV, XLS o XLSX.`)
      setRunSummary(null)
      return
    }

    setIsUploading(true)
    setErrorMessage(null)
    setRunSummary(null)

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
        throw new Error(detail ?? 'No se pudo procesar el archivo en el pipeline.')
      }
      registerUpload(files[0])
      setSelectedFileName(files[0].name)
      setSelectedFilesCount(files.length)
      setRunSummary(data as PipelineRunResponse)
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : 'Error inesperado durante la carga.')
    } finally {
      setIsUploading(false)
      event.target.value = ''
    }
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-5 lg:grid-cols-3">

        {/* Upload zone */}
        <div className="lg:col-span-2">
          <label
            htmlFor="data-file"
            className={`group relative flex cursor-pointer flex-col items-center justify-center gap-4 rounded-2xl border-2 border-dashed p-10 text-center transition-all duration-200 ${
              isUploading
                ? 'border-blue-300 bg-blue-50/60 cursor-wait'
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

            {/* Icon */}
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
                {isUploading ? 'Procesando archivo…' : 'Arrastra tu archivo aquí'}
              </p>
              <p className="mt-1 text-sm text-slate-500">
                {isUploading
                  ? 'Ejecutando pipeline ETL en el servidor'
                  : selectedFileName
                  ? `Seleccionado: ${selectedFileName}${selectedFilesCount > 1 ? ` (+${selectedFilesCount - 1} más)` : ''}`
                  : 'o haz clic para seleccionar desde tu equipo'}
              </p>
            </div>

            <div className="flex items-center gap-2">
              {['CSV', 'XLS', 'XLSX'].map((fmt) => (
                <span key={fmt} className="rounded-full bg-white px-2.5 py-0.5 text-xs font-semibold text-slate-500 shadow-sm ring-1 ring-slate-200">
                  {fmt}
                </span>
              ))}
            </div>

            {!isUploading && (
              <span className="rounded-xl bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white shadow-sm transition group-hover:bg-blue-700">
                Seleccionar archivo
              </span>
            )}
          </label>

          {/* Error */}
          {errorMessage && (
            <div className="mt-4 flex items-start gap-3 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3">
              <svg className="mt-0.5 h-4 w-4 shrink-0 text-rose-500" viewBox="0 0 24 24" fill="currentColor">
                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm-1 5h2v6h-2V7zm0 8h2v2h-2v-2z" clipRule="evenodd" />
              </svg>
              <p className="text-sm text-rose-700">{errorMessage}</p>
            </div>
          )}
        </div>

        {/* Status panel */}
        <div className="flex flex-col gap-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="mb-3 text-xs font-semibold uppercase tracking-widest text-blue-600">Estado</p>
            <div className="flex items-center gap-2.5">
              <span className={`h-2.5 w-2.5 rounded-full ${isUploading ? 'animate-pulse bg-blue-500' : lastUploadedFile ? 'bg-emerald-500' : 'bg-slate-300'}`} />
              <p className="text-sm font-medium text-slate-700">
                {isUploading
                  ? 'Procesando…'
                  : lastUploadedFile
                  ? 'Listo'
                  : 'Esperando archivo'}
              </p>
            </div>
            {lastUploadedFile && !isUploading && (
              <p className="mt-3 text-xs text-slate-400">Última carga: {uploadDate}</p>
            )}
          </div>

          <div className="rounded-2xl border border-slate-100 bg-slate-50 p-5">
            <p className="mb-2 text-xs font-semibold uppercase tracking-widest text-slate-400">Pipeline ETL</p>
            {['Bronze — Ingesta raw', 'Silver — Limpieza', 'Gold — Star Schema'].map((step, i) => (
              <div key={step} className="flex items-center gap-2.5 py-1.5">
                <span className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[10px] font-bold ${
                  runSummary ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-200 text-slate-500'
                }`}>
                  {i + 1}
                </span>
                <p className="text-xs text-slate-600">{step}</p>
              </div>
            ))}
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
            <div className="rounded-xl bg-white p-4 shadow-sm">
              <p className="text-2xl font-bold text-slate-800">{runSummary.rows_consolidated.toLocaleString()}</p>
              <p className="mt-1 text-xs text-slate-500">Registros consolidados</p>
            </div>
            <div className="rounded-xl bg-white p-4 shadow-sm">
              <p className="text-2xl font-bold text-slate-800">{runSummary.kpis_total}</p>
              <p className="mt-1 text-xs text-slate-500">KPIs generados</p>
            </div>
            <div className="rounded-xl bg-white p-4 shadow-sm">
              <p className="text-2xl font-bold text-slate-800">{Object.keys(runSummary.dimensions).length}</p>
              <p className="mt-1 text-xs text-slate-500">Dimensiones cargadas</p>
            </div>
            <div className="rounded-xl bg-white p-4 shadow-sm">
              <p className="text-2xl font-bold text-slate-800">{runSummary.warnings.length}</p>
              <p className="mt-1 text-xs text-slate-500">Advertencias</p>
            </div>
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
