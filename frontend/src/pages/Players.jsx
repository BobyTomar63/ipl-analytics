import { useState, useEffect } from "react"

const API_URL = "http://localhost:8000"

function Players() {
  const [batsmen, setBatsmen] = useState([])
  const [bowlers, setBowlers] = useState([])
  const [season, setSeason] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPlayers()
  }, [season])

  const fetchPlayers = async () => {
    setLoading(true)
    try {
      const url = season
        ? `${API_URL}/api/players/top-batsmen?season=${season}&limit=15`
        : `${API_URL}/api/players/top-batsmen?limit=15`

      const urlB = season
        ? `${API_URL}/api/players/top-bowlers?season=${season}&limit=15`
        : `${API_URL}/api/players/top-bowlers?limit=15`

      const [batRes, bowRes] = await Promise.all([
        fetch(url),
        fetch(urlB)
      ])

      const batData = await batRes.json()
      const bowData = await bowRes.json()

      setBatsmen(batData.players)
      setBowlers(bowData.players)
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setLoading(false)
    }
  }

  const seasons = Array.from(
    {length: 17}, (_, i) => 2007 + i
  )

  return (
    <div>
      {/* Header */}
      <div className="flex items-center 
                      justify-between mb-6">
        <h1 className="text-3xl font-bold text-white">
          👤 Players Stats
        </h1>

        {/* Season Filter */}
        <select
          value={season}
          onChange={e => setSeason(e.target.value)}
          className="bg-gray-700 text-white px-4 py-2 
                     rounded-lg border border-gray-600"
        >
          <option value="">All Seasons</option>
          {seasons.map(s => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <p className="text-white text-2xl">
            🏏 Loading Players...
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          {/* Top Batsmen */}
          <div className="bg-gray-800 rounded-xl p-6">
            <h2 className="text-xl font-bold 
                           text-orange-400 mb-4">
              🟠 Top Batsmen
              {season && ` — ${season}`}
            </h2>
            {batsmen.map(player => (
              <div key={player.rank}
                className="flex justify-between items-center
                           py-2 border-b border-gray-700">
                <div className="flex items-center gap-3">
                  <span className="text-gray-400 w-6">
                    {player.rank}
                  </span>
                  <div>
                    <p className="text-white font-medium">
                      {player.batsman}
                    </p>
                    <p className="text-gray-400 text-xs">
                      {player.matches} matches
                    </p>
                  </div>
                </div>
                <span className="text-orange-400 font-bold">
                  {player.total_runs} runs
                </span>
              </div>
            ))}
          </div>

          {/* Top Bowlers */}
          <div className="bg-gray-800 rounded-xl p-6">
            <h2 className="text-xl font-bold 
                           text-purple-400 mb-4">
              🟣 Top Bowlers
              {season && ` — ${season}`}
            </h2>
            {bowlers.map(player => (
              <div key={player.rank}
                className="flex justify-between items-center
                           py-2 border-b border-gray-700">
                <div className="flex items-center gap-3">
                  <span className="text-gray-400 w-6">
                    {player.rank}
                  </span>
                  <div>
                    <p className="text-white font-medium">
                      {player.bowler}
                    </p>
                    <p className="text-gray-400 text-xs">
                      {player.matches} matches
                    </p>
                  </div>
                </div>
                <span className="text-purple-400 font-bold">
                  {player.total_wickets} wkts
                </span>
              </div>
            ))}
          </div>

        </div>
      )}
    </div>
  )
}

export default Players