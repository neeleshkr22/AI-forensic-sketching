import { Link, useLocation } from 'react-router-dom'
import { Home, Image, Search, Database, Info } from 'lucide-react'

export default function Layout({ children }) {
  const location = useLocation()

  const navItems = [
    { path: '/', icon: Home, label: 'Home' },
    { path: '/sketch', icon: Image, label: 'Create Sketch' },
    { path: '/records', icon: Database, label: 'Records' },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Search className="w-8 h-8 text-primary-600" />
              <h1 className="text-2xl font-bold text-gray-800">
                AI Criminal Sketch Matcher
              </h1>
            </div>

            <nav className="hidden md:flex space-x-6">
              {navItems.map(({ path, icon: Icon, label }) => (
                <Link
                  key={path}
                  to={path}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                    location.pathname === path
                      ? 'bg-primary-100 text-primary-700'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{label}</span>
                </Link>
              ))}
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-auto">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center">
            <p className="text-sm">
              © 2025 AI Criminal Sketch Matcher. Built with AI for Law Enforcement.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
