import { useState, useEffect } from "react"

const API_URL = "http://localhost:8000"

function Matches() {
  const [matches, setMatches] = useState([])
  const [season, setSeason] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMatches()
  }, [season])

  const fetchMatches = async () => {
    setLoading(true)
    try {
      const url = season
        ? `${API_URL}/api/matches/?season=${season}&limit=50`
        : `${API_URL}/api/matches/?limit=50`

      const res = await fetch(url)
      const data = await res.json()
      setMatches(data.matches)
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
          🎯 Matches
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
            🏏 Loading Matches...
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {matches.map(match => (
            <div key={match.match_id}
              className="bg-gray-800 rounded-xl p-5
                         hover:bg-gray-700 transition-all">

              {/* Match Header */}
              <div className="flex justify-between 
                              items-center mb-3">
                <span className="text-gray-400 text-sm">
                  📅 {match.date} | Season {match.season}
                </span>
                <span className="text-gray-400 text-sm">
                  📍 {match.venue}
                </span>
              </div>

              {/* Teams */}
              <div className="flex items-center 
                              justify-between">
                <div className="text-center flex-1">
                  <p className={`text-lg font-bold
                    ${match.winner === match.team1
                      ? 'text-green-400'
                      : 'text-white'
                    }`}>
                    {match.team1}
                  </p>
                  {match.winner === match.team1 && (
                    <span className="text-green-400 
                                     text-xs">
                      ✅ Winner
                    </span>
                  )}
                </div>

                <div className="text-center px-4">
                  <p className="text-gray-400 text-xl 
                                font-bold">VS</p>
                </div>

                <div className="text-center flex-1">
                  <p className={`text-lg font-bold
                    ${match.winner === match.team2
                      ? 'text-green-400'
                      : 'text-white'
                    }`}>
                    {match.team2}
                  </p>
                  {match.winner === match.team2 && (
                    <span className="text-green-400 
                                     text-xs">
                      ✅ Winner
                    </span>
                  )}
                </div>
              </div>

              {/* Match Result */}
              <div className="mt-3 pt-3 
                              border-t border-gray-700
                              flex justify-between">
                <span className="text-gray-400 text-sm">
                  🏆 {match.winner}
                </span>
                <span className="text-gray-400 text-sm">
                  ⭐ {match.player_of_match}
                </span>
              </div>

            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Matches