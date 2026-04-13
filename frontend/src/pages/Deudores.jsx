import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { listarDeudores, generarScript, generarAudio, llamarDeudor, audioUrl } from '../api'

const estadoColor = {
  pendiente: 'bg-gray-100 text-gray-700',
  script_generado: 'bg-blue-100 text-blue-700',
  audio_generado: 'bg-purple-100 text-purple-700',
  llamado: 'bg-yellow-100 text-yellow-700',
  contesto: 'bg-green-100 text-green-700',
  no_contesto: 'bg-red-100 text-red-700',
}

const estadoLabel = {
  pendiente: 'Pendiente',
  script_generado: 'Script generado',
  audio_generado: 'Audio generado',
  llamado: 'Llamado',
  contesto: 'Contestó',
  no_contesto: 'No contestó',
}

function formatMonto(n) {
  return '$' + Number(n).toLocaleString('es-CL', { maximumFractionDigits: 0 })
}

export default function Deudores() {
  const [deudores, setDeudores] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState({})
  const [error, setError] = useState('')
  const [audioPlaying, setAudioPlaying] = useState(null)

  const cargar = () => {
    listarDeudores()
      .then(d => { setDeudores(d); setLoading(false) })
      .catch(e => { setError(e.message); setLoading(false) })
  }

  useEffect(() => { cargar() }, [])

  const handleAction = async (id, action, label) => {
    setActionLoading(prev => ({ ...prev, [id]: label }))
    try {
      await action(id)
      cargar()
    } catch (e) {
      alert(`Error: ${e.message}`)
    } finally {
      setActionLoading(prev => ({ ...prev, [id]: null }))
    }
  }

  if (loading) return <p className="text-gray-500">Cargando deudores...</p>
  if (error) return <p className="text-red-600">Error: {error}</p>

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Deudores</h1>

      {deudores.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-xl shadow">
          <p className="text-gray-500 mb-4">No hay deudores registrados</p>
          <Link to="/upload" className="text-indigo-600 hover:underline font-medium">
            Cargar CSV
          </Link>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {['Nombre', 'RUT', 'Teléfono', 'Monto', 'Días Mora', 'Estado', 'Acciones'].map(h => (
                    <th key={h} className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {deudores.map(d => (
                  <tr key={d.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <Link to={`/deudores/${d.id}`} className="text-indigo-600 hover:underline font-medium">
                        {d.nombre}
                      </Link>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">{d.rut}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{d.telefono}</td>
                    <td className="px-4 py-3 text-sm font-medium">{formatMonto(d.monto_deuda)}</td>
                    <td className="px-4 py-3 text-sm">
                      <span className={`font-medium ${d.dias_mora >= 60 ? 'text-red-600' : d.dias_mora >= 30 ? 'text-yellow-600' : 'text-gray-600'}`}>
                        {d.dias_mora}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${estadoColor[d.estado] || 'bg-gray-100 text-gray-700'}`}>
                        {estadoLabel[d.estado] || d.estado}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2 flex-wrap">
                        {d.estado === 'pendiente' && (
                          <button
                            onClick={() => handleAction(d.id, generarScript, 'script')}
                            disabled={!!actionLoading[d.id]}
                            className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white text-xs px-3 py-1 rounded transition-colors"
                          >
                            {actionLoading[d.id] === 'script' ? '...' : 'Generar Script'}
                          </button>
                        )}
                        {d.estado === 'script_generado' && (
                          <button
                            onClick={() => handleAction(d.id, generarAudio, 'audio')}
                            disabled={!!actionLoading[d.id]}
                            className="bg-purple-500 hover:bg-purple-600 disabled:bg-gray-300 text-white text-xs px-3 py-1 rounded transition-colors"
                          >
                            {actionLoading[d.id] === 'audio' ? '...' : 'Generar Audio'}
                          </button>
                        )}
                        {(d.estado === 'audio_generado' || d.estado === 'no_contesto') && (
                          <button
                            onClick={() => handleAction(d.id, llamarDeudor, 'llamar')}
                            disabled={!!actionLoading[d.id]}
                            className="bg-green-500 hover:bg-green-600 disabled:bg-gray-300 text-white text-xs px-3 py-1 rounded transition-colors"
                          >
                            {actionLoading[d.id] === 'llamar' ? '...' : 'Llamar'}
                          </button>
                        )}
                        {d.audio_path && (
                          <button
                            onClick={() => setAudioPlaying(audioPlaying === d.id ? null : d.id)}
                            className="bg-gray-200 hover:bg-gray-300 text-gray-700 text-xs px-3 py-1 rounded transition-colors"
                          >
                            {audioPlaying === d.id ? 'Cerrar' : 'Escuchar'}
                          </button>
                        )}
                      </div>
                      {audioPlaying === d.id && (
                        <audio controls autoPlay className="mt-2 w-full h-8" src={audioUrl(d.id)} />
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
