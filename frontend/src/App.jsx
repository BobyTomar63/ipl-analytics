import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Teams from './pages/Teams'
import Players from './pages/Players'
import Matches from './pages/Matches'

function App() {
  return (
    <div className="min-h-screen bg-gray-900">
      <Navbar />
      <div className="max-w-7xl mx-auto p-6">
        <Routes>
          <Route path="/"        element={<Dashboard />} />
          <Route path="/teams"   element={<Teams />}     />
          <Route path="/players" element={<Players />}   />
          <Route path="/matches" element={<Matches />}   />
        </Routes>
      </div>
    </div>
  )
}

export default App