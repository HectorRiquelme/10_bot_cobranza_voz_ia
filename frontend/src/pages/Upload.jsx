import { useState, useRef } from 'react'
import { uploadCSV } from '../api'
import { useNavigate } from 'react-router-dom'

export default function Upload() {
  const [archivo, setArchivo] = useState(null)
  const [cargando, setCargando] = useState(false)
  const [mensaje, setMensaje] = useState('')
  const [error, setError] = useState('')
  const inputRef = useRef()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!archivo) return
    setCargando(true)
    setError('')
    setMensaje('')
    try {
      const res = await uploadCSV(archivo)
      setMensaje(res.mensaje)
      setArchivo(null)
      if (inputRef.current) inputRef.current.value = ''
      setTimeout(() => navigate('/deudores'), 1500)
    } catch (e) {
      setError(e.message)
    } finally {
      setCargando(false)
    }
  }

  return (
    <div className="max-w-xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Cargar Deudores</h1>

      <div className="bg-white rounded-xl shadow-md p-8">
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Archivo CSV
            </label>
            <input
              ref={inputRef}
              type="file"
              accept=".csv"
              onChange={e => setArchivo(e.target.files[0])}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
            />
            <p className="mt-2 text-xs text-gray-400">
              Columnas requeridas: nombre, rut, telefono, monto_deuda, dias_mora, email
            </p>
          </div>

          <button
            type="submit"
            disabled={!archivo || cargando}
            className="w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white font-medium py-3 px-4 rounded-lg transition-colors"
          >
            {cargando ? 'Cargando...' : 'Subir CSV'}
          </button>
        </form>

        {mensaje && (
          <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg text-green-700">
            {mensaje}
          </div>
        )}
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}
      </div>
    </div>
  )
}
