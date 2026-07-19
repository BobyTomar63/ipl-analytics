import { useState, useEffect } from "react"

const API_URL = "https://ipl-analytics-backend-kbfv.onrender.com"

function Teams() {
  const [teams, setTeams] = useState([])
  const [selectedTeam, setSelectedTeam] = useState(null)
  const [teamStats, setTeamStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [statsLoading, setStatsLoading] = useState(false)

  useEffect(() => {
    fetchTeams()
  }, [])

  const fetchTeams = async () => {
    try {
      const res = await fetch(`${API_URL}/api/teams/`)
      const data = await res.json()
      setTeams(data.teams)
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setLoading(false)
    }
  }

  const fetchTeamStats = async (team) => {
    setStatsLoading(true)
    setSelectedTeam(team)
    try {
      const res = await fetch(
        `${API_URL}/api/teams/${encodeURIComponent(team)}/stats`
      )
      const data = await res.json()
      setTeamStats(data.stats)
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setStatsLoading(false)
    }
  }

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <p className="text-white text-2xl">🏏 Loading Teams...</p>
    </div>
  )

  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-6">
        🏆 IPL Teams
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* Teams List */}
        <div className="bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-bold text-white mb-4">
            All Teams ({teams.length})
          </h2>
          <div className="space-y-2">
            {teams.map(team => (
              <button
                key={team}
                onClick={() => fetchTeamStats(team)}
                className={`w-full text-left px-4 py-3 rounded-lg
                  transition-all font-medium
                  ${selectedTeam === team
                    ? 'bg-orange-500 text-white'
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                  }`}
              >
                🏏 {team}
              </button>
            ))}
          </div>
        </div>

        {/* Team Stats */}
        <div className="bg-gray-800 rounded-xl p-6">
          {!selectedTeam ? (
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-400 text-center">
                👈 Koi team select karo<br/>
                stats dekhne ke liye
              </p>
            </div>
          ) : statsLoading ? (
            <div className="flex items-center justify-center h-full">
              <p className="text-white">Loading stats...</p>
            </div>
          ) : teamStats && (
            <div>
              <h2 className="text-xl font-bold text-orange-400 mb-6">
                {selectedTeam}
              </h2>

              {/* Stats Cards */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-blue-900 rounded-xl p-4 text-center">
                  <p className="text-3xl font-bold text-white">
                    {teamStats.total_matches}
                  </p>
                  <p className="text-blue-300 text-sm mt-1">
                    Total Matches
                  </p>
                </div>
                <div className="bg-green-900 rounded-xl p-4 text-center">
                  <p className="text-3xl font-bold text-white">
                    {teamStats.wins}
                  </p>
                  <p className="text-green-300 text-sm mt-1">
                    Wins
                  </p>
                </div>
                <div className="bg-red-900 rounded-xl p-4 text-center">
                  <p className="text-3xl font-bold text-white">
                    {teamStats.losses}
                  </p>
                  <p className="text-red-300 text-sm mt-1">
                    Losses
                  </p>
                </div>
                <div className="bg-orange-900 rounded-xl p-4 text-center">
                  <p className="text-3xl font-bold text-white">
                    {teamStats.win_percentage}%
                  </p>
                  <p className="text-orange-300 text-sm mt-1">
                    Win Rate
                  </p>
                </div>
              </div>

              {/* Win Rate Bar */}
              <div>
                <p className="text-gray-400 text-sm mb-2">
                  Win Rate
                </p>
                <div className="bg-gray-700 rounded-full h-4">
                  <div
                    className="bg-orange-500 rounded-full h-4 
                               transition-all duration-500"
                    style={{width: `${teamStats.win_percentage}%`}}
                  />
                </div>
                <p className="text-orange-400 text-sm mt-1 text-right">
                  {teamStats.win_percentage}%
                </p>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

export default Teams