const powerBiEmbedUrl =
  import.meta.env.VITE_POWERBI_EMBED_URL ??
  'https://app.powerbi.com/view?r=eyJrIjoiMDMyOTFmZWUtYTIwNC00YmJkLWI4MGUtMDZkMjUwMTVjZDUxIiwidCI6IjRkZDEzM2ZkLWNhMmEtNDA5OC1hZTkxLTBlYWEwYzU4MjNiOCIsImMiOjR9'

export function DashboardPage() {
  return (
    <section className="space-y-4">
      <p className="text-sm text-slate-600">
        Aqui se visualizan los indicadores consolidados del pipeline mediante Power BI embebido.
      </p>

      <div className="overflow-hidden rounded-2xl border border-slate-200">
        <iframe
          title="Dashboard Power BI"
          src={powerBiEmbedUrl}
          className="h-[420px] w-full bg-slate-50 sm:h-[520px]"
          loading="lazy"
        />
      </div>
    </section>
  )
}
