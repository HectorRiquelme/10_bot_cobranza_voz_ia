import { Routes, Route, Link, useLocation } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Deudores from './pages/Deudores'
import DetalleDeudor from './pages/DetalleDeudor'
import Upload from './pages/Upload'

const navItems = [
  { to: '/', label: 'Dashboard' },
  { to: '/deudores', label: 'Deudores' },
  { to: '/upload', label: 'Cargar CSV' },
]

export default function App() {
  const location = useLocation()

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-indigo-700 shadow-lg">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="text-white font-bold text-xl">
              Cobranza Voz IA
            </Link>
            <div className="flex space-x-4">
              {navItems.map(item => (
                <Link
                  key={item.to}
                  to={item.to}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    location.pathname === item.to
                      ? 'bg-indigo-900 text-white'
                      : 'text-indigo-200 hover:bg-indigo-600 hover:text-white'
                  }`}
                >
                  {item.label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/deudores" element={<Deudores />} />
          <Route path="/deudores/:id" element={<DetalleDeudor />} />
          <Route path="/upload" element={<Upload />} />
        </Routes>
      </main>
    </div>
  )
}
