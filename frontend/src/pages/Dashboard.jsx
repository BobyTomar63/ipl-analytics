import { useState, useEffect } from "react"

const API_URL = "http://localhost:8000"

function Dashboard() {
  const [overview, setOverview] = useState(null)
  const [orangeCap, setOrangeCap] = useState([])
  const [purpleCap, setPurpleCap] = useState([])
  const [toss, setToss] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [overviewRes, orangeRes, purpleRes, tossRes] = 
        await Promise.all([
          fetch(`${API_URL}/api/dashboard/overview`),
          fetch(`${API_URL}/api/dashboard/orange-cap`),
          fetch(`${API_URL}/api/dashboard/purple-cap`),
          fetch(`${API_URL}/api/dashboard/toss-analysis`),
        ])

      const overviewData = await overviewRes.json()
      const orangeData   = await orangeRes.json()
      const purpleData   = await purpleRes.json()
      const tossData     = await tossRes.json()

      setOverview(overviewData.overview)
      setOrangeCap(orangeData.orange_cap)
      setPurpleCap(purpleData.purple_cap)
      setToss(tossData.toss_analysis)
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <p className="text-white text-2xl">🏏 Loading...</p>
    </div>
  )

  return (
    <div>
      {/* Overview Cards */}
      {overview && (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          {[
            { label: "Total Matches", value: overview.total_matches, color: "blue"   },
            { label: "Seasons",       value: overview.total_seasons, color: "green"  },
            { label: "Teams",         value: overview.total_teams,   color: "purple" },
            { label: "Total Runs",    value: overview.total_runs.toLocaleString(), color: "orange" },
            { label: "Wickets",       value: overview.total_wickets.toLocaleString(), color: "red" },
          ].map(card => (
            <div key={card.label}
              className={`bg-${card.color}-900 rounded-xl p-4 text-center`}>
              <p className="text-3xl font-bold text-white">
                {card.value}
              </p>
              <p className={`text-${card.color}-300 text-sm mt-1`}>
                {card.label}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Orange & Purple Cap */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">

        {/* Orange Cap */}
        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-bold text-orange-400 mb-4">
            🟠 Orange Cap — Top Batsmen
          </h2>
          {orangeCap.map(player => (
            <div key={player.rank}
              className="flex justify-between items-center
                         py-2 border-b border-gray-700">
              <div className="flex items-center gap-3">
                <span className="text-gray-400 w-6">{player.rank}</span>
                <span className="text-white">{player.batsman}</span>
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
          {purpleCap.map(player => (
            <div key={player.rank}
              className="flex justify-between items-center
                         py-2 border-b border-gray-700">
              <div className="flex items-center gap-3">
                <span className="text-gray-400 w-6">{player.rank}</span>
                <span className="text-white">{player.bowler}</span>
              </div>
              <span className="text-purple-400 font-bold">
                {player.wickets} wkts
              </span>
            </div>
          ))}
        </div>

      </div>

      {/* Toss Analysis */}
      <div className="bg-gray-800 rounded-xl p-6">
        <h2 className="text-xl font-bold text-white mb-4">
          🪙 Toss Analysis
        </h2>
        <div className="grid grid-cols-2 gap-4">
          {toss.map(item => (
            <div key={item.decision}
              className="bg-gray-700 rounded-xl p-4 text-center">
              <p className="text-2xl font-bold text-white capitalize">
                {item.decision} First
              </p>
              <p className="text-gray-400 mt-1">
                {item.total} matches
              </p>
              <p className="text-green-400 font-bold text-xl mt-2">
                {item.win_percentage}% wins
              </p>
            </div>
          ))}
        </div>
      </div>

    </div>
  )
}

export default Dashboard