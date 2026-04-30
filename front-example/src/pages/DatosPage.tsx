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
    if (!lastUploadedFile) {
      return null
    }
    return new Date(lastUploadedFile.uploadedAt).toLocaleString('es-CO')
  }, [lastUploadedFile])

  const handleFileChange = async (event: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files ?? [])
    if (files.length === 0) {
      return
    }

    const supportedTypes = ['.csv', '.xlsx', '.xls']
    const invalidFile = files.find((currentFile) => {
      const extension = currentFile.name.slice(currentFile.name.lastIndexOf('.')).toLowerCase()
      return !supportedTypes.includes(extension)
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
    files.forEach((currentFile) => {
      formData.append('files', currentFile)
    })

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
    <section className="grid gap-6 lg:grid-cols-3">
      <div className="rounded-2xl border border-blue-100 bg-blue-50/70 p-5 lg:col-span-2">
        <h3 className="text-lg font-semibold text-slate-800">Subir archivo de Datos</h3>
        <p className="mt-1 text-sm text-slate-600">
          Carga uno o varios archivos CSV/XLS/XLSX para ejecutar limpieza, transformacion y consolidacion.
        </p>

        <label
          htmlFor="data-file"
          className="mt-5 inline-flex cursor-pointer items-center rounded-xl bg-blue-700 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-800"
        >
          {isUploading ? 'Procesando...' : 'Seleccionar archivo'}
        </label>
        <input
          id="data-file"
          type="file"
          accept=".csv,.xls,.xlsx"
          multiple
          className="hidden"
          onChange={handleFileChange}
          disabled={isUploading}
        />

        <p className="mt-3 text-sm text-slate-700">
          {selectedFileName
            ? selectedFilesCount > 1
              ? `Archivos seleccionados: ${selectedFilesCount} (ejemplo: ${selectedFileName})`
              : `Archivo seleccionado: ${selectedFileName}`
            : 'No hay archivo seleccionado'}
        </p>
        <p className="mt-1 text-xs text-slate-500">Formatos soportados: CSV, XLS y XLSX</p>

        {isUploading && (
          <p className="mt-3 text-sm font-medium text-blue-700">Subiendo archivo y ejecutando pipeline...</p>
        )}

        {errorMessage && (
          <p className="mt-3 rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">
            {errorMessage}
          </p>
        )}
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5">
        <p className="text-xs font-semibold uppercase tracking-wide text-blue-700">Estado</p>
        <p className="mt-2 text-sm text-slate-600">
          {isUploading
            ? 'Procesando archivo en el pipeline...'
            : lastUploadedFile
              ? 'Archivo cargado y procesado.'
              : 'Esperando carga de archivo.'}
        </p>
      </div>

      {runSummary && (
        <div className="rounded-2xl border border-blue-200 bg-blue-50 p-5 text-sm text-blue-900 lg:col-span-3">
          <p className="font-semibold">Resultado del procesamiento</p>
          <p className="mt-1">Registros consolidados: {runSummary.rows_consolidated}</p>
          <p>KPIs generados: {runSummary.kpis_total}</p>
          <p className="mt-2 font-medium">Dimensiones cargadas:</p>
          <ul className="mt-1 list-disc pl-5">
            {Object.entries(runSummary.dimensions).map(([key, value]) => (
              <li key={key}>
                {key}: {value}
              </li>
            ))}
          </ul>
          {runSummary.warnings.length > 0 && (
            <p className="mt-2 text-xs text-blue-800">Advertencias: {runSummary.warnings.join(' | ')}</p>
          )}
        </div>
      )}

      {lastUploadedFile && (
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-5 text-sm text-emerald-900 lg:col-span-3">
          <p className="font-semibold">Ultima carga registrada</p>
          <p className="mt-1">Archivo: {lastUploadedFile.name}</p>
          <p>Tamano: {(lastUploadedFile.size / 1024).toFixed(1)} KB</p>
          <p>Tipo: {lastUploadedFile.type}</p>
          <p>Fecha: {uploadDate}</p>
        </div>
      )}
    </section>
  )
}
