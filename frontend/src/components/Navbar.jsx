import { Link, useLocation } from 'react-router-dom'

function Navbar() {
  const location = useLocation()

  const links = [
    { path: '/',        label: '📊 Dashboard' },
    { path: '/teams',   label: '🏏 Teams'     },
    { path: '/players', label: '👤 Players'   },
    { path: '/matches', label: '🎯 Matches'   },
  ]

  return (
    <nav className="bg-gray-800 border-b border-gray-700 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Logo */}
        <Link to="/" className="text-2xl font-bold text-white">
          🏏 IPL Analytics
        </Link>

        {/* Links */}
        <div className="flex gap-6">
          {links.map(link => (
            <Link
              key={link.path}
              to={link.path}
              className={`px-4 py-2 rounded-lg font-medium transition-all
                ${location.pathname === link.path
                  ? 'bg-orange-500 text-white'
                  : 'text-gray-300 hover:text-white hover:bg-gray-700'
                }`}
            >
              {link.label}
            </Link>
          ))}
        </div>

      </div>
    </nav>
  )
}

export default Navbar