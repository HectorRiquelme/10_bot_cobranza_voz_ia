import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { detalleDeudor, generarScript, generarAudio, llamarDeudor, audioUrl } from '../api'

function formatMonto(n) {
  return '$' + Number(n).toLocaleString('es-CL', { maximumFractionDigits: 0 })
}

export default function DetalleDeudor() {
  const { id } = useParams()
  const [deudor, setDeudor] = useState(null)
  const [loading, setLoading] = useState(true)
  const [actionMsg, setActionMsg] = useState('')
  const [actionLoading, setActionLoading] = useState(false)

  const cargar = () => {
    detalleDeudor(id)
      .then(d => { setDeudor(d); setLoading(false) })
      .catch(() => setLoading(false))
  }

  useEffect(() => { cargar() }, [id])

  const handleAction = async (action, label) => {
    setActionLoading(true)
    setActionMsg('')
    try {
      const res = await action(id)
      setActionMsg(res.mensaje)
      cargar()
    } catch (e) {
      setActionMsg(`Error: ${e.message}`)
    } finally {
      setActionLoading(false)
    }
  }

  if (loading) return <p className="text-gray-500">Cargando...</p>
  if (!deudor) return <p className="text-red-600">Deudor no encontrado</p>

  return (
    <div>
      <Link to="/deudores" className="text-indigo-600 hover:underline text-sm mb-4 inline-block">
        &larr; Volver a deudores
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Info principal */}
        <div className="lg:col-span-2 bg-white rounded-xl shadow-md p-6">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">{deudor.nombre}</h1>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div><span className="text-gray-500">RUT:</span> <span className="font-medium">{deudor.rut}</span></div>
            <div><span className="text-gray-500">Teléfono:</span> <span className="font-medium">{deudor.telefono}</span></div>
            <div><span className="text-gray-500">Monto deuda:</span> <span className="font-bold text-red-600">{formatMonto(deudor.monto_deuda)}</span></div>
            <div><span className="text-gray-500">Días de mora:</span> <span className="font-bold">{deudor.dias_mora}</span></div>
            <div><span className="text-gray-500">Email:</span> <span className="font-medium">{deudor.email || 'N/A'}</span></div>
            <div><span className="text-gray-500">Estado:</span> <span className="font-semibold capitalize">{deudor.estado.replace('_', ' ')}</span></div>
          </div>

          {/* Acciones */}
          <div className="mt-6 flex gap-3 flex-wrap">
            <button
              onClick={() => handleAction(generarScript)}
              disabled={actionLoading}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              Generar Script
            </button>
            <button
              onClick={() => handleAction(generarAudio)}
              disabled={actionLoading || !deudor.script}
              className="bg-purple-500 hover:bg-purple-600 disabled:bg-gray-300 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              Generar Audio
            </button>
            <button
              onClick={() => handleAction(llamarDeudor)}
              disabled={actionLoading || !deudor.audio_path}
              className="bg-green-500 hover:bg-green-600 disabled:bg-gray-300 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              Realizar Llamada
            </button>
          </div>

          {actionMsg && (
            <p className={`mt-3 text-sm ${actionMsg.startsWith('Error') ? 'text-red-600' : 'text-green-600'}`}>
              {actionMsg}
            </p>
          )}

          {/* Script */}
          {deudor.script && (
            <div className="mt-6">
              <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Script de Cobranza</h3>
              <div className="bg-gray-50 rounded-lg p-4 text-sm text-gray-700 whitespace-pre-wrap">
                {deudor.script}
              </div>
            </div>
          )}

          {/* Audio */}
          {deudor.audio_path && (
            <div className="mt-6">
              <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Audio Generado</h3>
              <audio controls className="w-full" src={audioUrl(deudor.id)} />
            </div>
          )}
        </div>

        {/* Historial */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Historial</h2>
          {deudor.historial.length === 0 ? (
            <p className="text-gray-400 text-sm">Sin actividad registrada</p>
          ) : (
            <div className="space-y-3">
              {deudor.historial.map(h => (
                <div key={h.id} className="border-l-2 border-indigo-300 pl-3">
                  <p className="text-sm font-medium text-gray-700 capitalize">
                    {h.accion.replace(/_/g, ' ')}
                  </p>
                  {h.detalle && <p className="text-xs text-gray-500">{h.detalle}</p>}
                  <p className="text-xs text-gray-400">{h.created_at}</p>
                </div>
              ))}
            </div>
          )}

          {deudor.llamadas.length > 0 && (
            <>
              <h3 className="text-lg font-bold text-gray-800 mt-6 mb-4">Llamadas</h3>
              <div className="space-y-3">
                {deudor.llamadas.map(l => (
                  <div key={l.id} className="bg-gray-50 rounded-lg p-3 text-sm">
                    <p><span className="text-gray-500">Estado:</span> <span className="font-medium capitalize">{l.estado}</span></p>
                    <p><span className="text-gray-500">Duración:</span> {l.duracion}s</p>
                    <p><span className="text-gray-500">Contestada:</span> {l.contestada ? 'Sí' : 'No'}</p>
                    <p className="text-xs text-gray-400 mt-1">{l.created_at}</p>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
