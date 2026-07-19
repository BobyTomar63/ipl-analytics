import { useState, useEffect } from "react"

const API_URL = "http://localhost:8000"

function App() {
  const [overview, setOverview] = useState(null)
  const [orangeCap, setOrangeCap] = useState([])
  const [purpleCap, setPurpleCap] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [overviewRes, orangeRes, purpleRes] = await Promise.all([
        fetch(`${API_URL}/api/dashboard/overview`),
        fetch(`${API_URL}/api/dashboard/orange-cap`),
        fetch(`${API_URL}/api/dashboard/purple-cap`)
      ])

      const overviewData = await overviewRes.json()
      const orangeData = await orangeRes.json()
      const purpleData = await purpleRes.json()

      setOverview(overviewData.overview)
      setOrangeCap(orangeData.orange_cap)
      setPurpleCap(purpleData.purple_cap)
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return (
    <div className="min-h-screen bg-gray-900 
                    flex items-center justify-center">
      <p className="text-white text-2xl">
        🏏 Loading IPL Data...
      </p>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-900 p-6">

      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white">
          🏏 IPL Analytics
        </h1>
        <p className="text-gray-400 mt-2">
          Complete IPL Data Analysis Platform
        </p>
      </div>

      {/* Overview Cards */}
      {overview && (
        <div className="grid grid-cols-2 md:grid-cols-5 
                        gap-4 mb-8">
          <div className="bg-blue-900 rounded-xl p-4 text-center">
            <p className="text-3xl font-bold text-white">
              {overview.total_matches}
            </p>
            <p className="text-blue-300 text-sm mt-1">
              Total Matches
            </p>
          </div>
          <div className="bg-green-900 rounded-xl p-4 text-center">
            <p className="text-3xl font-bold text-white">
              {overview.total_seasons}
            </p>
            <p className="text-green-300 text-sm mt-1">
              Seasons
            </p>
          </div>
          <div className="bg-purple-900 rounded-xl p-4 text-center">
            <p className="text-3xl font-bold text-white">
              {overview.total_teams}
            </p>
            <p className="text-purple-300 text-sm mt-1">
              Teams
            </p>
          </div>
          <div className="bg-orange-900 rounded-xl p-4 text-center">
            <p className="text-3xl font-bold text-white">
              {overview.total_runs.toLocaleString()}
            </p>
            <p className="text-orange-300 text-sm mt-1">
              Total Runs
            </p>
          </div>
          <div className="bg-red-900 rounded-xl p-4 text-center">
            <p className="text-3xl font-bold text-white">
              {overview.total_wickets.toLocaleString()}
            </p>
            <p className="text-red-300 text-sm mt-1">
              Total Wickets
            </p>
          </div>
        </div>
      )}

      {/* Orange & Purple Cap */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* Orange Cap */}
        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-bold text-orange-400 mb-4">
            🟠 Orange Cap — Top Batsmen
          </h2>
          {orangeCap.map((player) => (
            <div key={player.rank}
              className="flex justify-between items-center 
                         py-2 border-b border-gray-700">
              <div className="flex items-center gap-3">
                <span className="text-gray-400 w-6">
                  {player.rank}
                </span>
                <span className="text-white">
                  {player.batsman}
                </span>
              </div>
              <span className="text-orange-400 font-bold">
                {player.runs} runs
              </span>
            </div>
          ))}
        </div>

        {/* Purple Cap */}
        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-bold text-purple-400 mb-4">
            🟣 Purple Cap — Top Bowlers
          </h2>
          {purpleCap.map((player) => (
            <div key={player.rank}
              className="flex justify-between items-center 
                         py-2 border-b border-gray-700">
              <div className="flex items-center gap-3">
                <span className="text-gray-400 w-6">
                  {player.rank}
                </span>
                <span className="text-white">
                  {player.bowler}
                </span>
              </div>
              <span className="text-purple-400 font-bold">
                {player.wickets} wkts
              </span>
            </div>
          ))}
        </div>

      </div>
    </div>
  )
}

export default App