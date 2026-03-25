import { useMemo, useState } from 'react'
import type { ChangeEvent } from 'react'
import { usePortalStore } from '../store/usePortalStore'

export function DatosPage() {
  const registerUpload = usePortalStore((state) => state.registerUpload)
  const lastUploadedFile = usePortalStore((state) => state.lastUploadedFile)
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null)

  const uploadDate = useMemo(() => {
    if (!lastUploadedFile) {
      return null
    }
    return new Date(lastUploadedFile.uploadedAt).toLocaleString('es-CO')
  }, [lastUploadedFile])

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) {
      return
    }
    registerUpload(file)
    setSelectedFileName(file.name)
  }

  return (
    <section className="grid gap-6 lg:grid-cols-3">
      <div className="rounded-2xl border border-blue-100 bg-blue-50/70 p-5 lg:col-span-2">
        <h3 className="text-lg font-semibold text-slate-800">Subir archivo de Datos</h3>
        <p className="mt-1 text-sm text-slate-600">
          Carga archivos CSV, XLSX o JSON para ejecutar limpieza, transformacion y consolidacion.
        </p>

        <label
          htmlFor="data-file"
          className="mt-5 inline-flex cursor-pointer items-center rounded-xl bg-blue-700 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-800"
        >
          Seleccionar archivo
        </label>
        <input id="data-file" type="file" className="hidden" onChange={handleFileChange} />

        <p className="mt-3 text-sm text-slate-700">
          {selectedFileName ? `Archivo seleccionado: ${selectedFileName}` : 'No hay archivo seleccionado'}
        </p>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5">
        <p className="text-xs font-semibold uppercase tracking-wide text-blue-700">Estado</p>
        <p className="mt-2 text-sm text-slate-600">
          {lastUploadedFile ? 'Archivo recibido. Listo para procesamiento.' : 'Esperando carga de archivo.'}
        </p>
      </div>

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
