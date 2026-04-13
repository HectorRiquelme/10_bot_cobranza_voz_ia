import { useState, useEffect } from 'react'
import { obtenerMetricas, exportarExcelUrl } from '../api'

function formatMonto(n) {
  return '$' + Number(n).toLocaleString('es-CL', { maximumFractionDigits: 0 })
}

export default function Dashboard() {
  const [metricas, setMetricas] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    obtenerMetricas()
      .then(setMetricas)
      .catch(e => setError(e.message))
  }, [])

  if (error) return <p className="text-red-600">Error: {error}</p>
  if (!metricas) return <p className="text-gray-500">Cargando métricas...</p>

  const cards = [
    { label: 'Total Deudores', value: metricas.total_deudores, color: 'bg-blue-500' },
    { label: 'Total Llamados', value: metricas.total_llamados, color: 'bg-yellow-500' },
    { label: 'Tasa Contestación', value: `${metricas.tasa_contestacion}%`, color: 'bg-green-500' },
    { label: 'Monto Total en Mora', value: formatMonto(metricas.monto_total_mora), color: 'bg-red-500' },
  ]

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>
        <a
          href={exportarExcelUrl()}
          className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          download
        >
          Exportar Excel
        </a>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {cards.map(card => (
          <div key={card.label} className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className={`${card.color} h-2`} />
            <div className="p-6">
              <p className="text-sm text-gray-500 uppercase tracking-wide">{card.label}</p>
              <p className="text-3xl font-bold text-gray-800 mt-2">{card.value}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
