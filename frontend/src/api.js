const BASE = '/api'

async function request(url, options = {}) {
  const res = await fetch(url, options)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Error del servidor' }))
    throw new Error(err.detail || `Error ${res.status}`)
  }
  return res
}

export async function uploadCSV(file) {
  const form = new FormData()
  form.append('archivo', file)
  const res = await request(`${BASE}/deudores/upload`, { method: 'POST', body: form })
  return res.json()
}

export async function listarDeudores() {
  const res = await request(`${BASE}/deudores`)
  return res.json()
}

export async function detalleDeudor(id) {
  const res = await request(`${BASE}/deudores/${id}`)
  return res.json()
}

export async function generarScript(id) {
  const res = await request(`${BASE}/cobranza/generar-script/${id}`, { method: 'POST' })
  return res.json()
}

export async function generarAudio(id) {
  const res = await request(`${BASE}/cobranza/generar-audio/${id}`, { method: 'POST' })
  return res.json()
}

export async function llamarDeudor(id) {
  const res = await request(`${BASE}/cobranza/llamar/${id}`, { method: 'POST' })
  return res.json()
}

export async function obtenerMetricas() {
  const res = await request(`${BASE}/metricas`)
  return res.json()
}

export function audioUrl(id) {
  return `${BASE}/audio/${id}`
}

export function exportarExcelUrl() {
  return `${BASE}/exportar/excel`
}
