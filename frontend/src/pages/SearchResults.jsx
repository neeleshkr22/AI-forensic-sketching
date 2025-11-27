import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { Search, Loader, AlertCircle, ChevronRight, Filter } from 'lucide-react'
import toast from 'react-hot-toast'
import { sketchAPI } from '../services/api'

export default function SearchResults() {
  const location = useLocation()
  const navigate = useNavigate()
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTime, setSearchTime] = useState(0)
  const [threshold, setThreshold] = useState(0.5)
  const [sketchData, setSketchData] = useState(location.state?.sketchData)

  useEffect(() => {
    if (!sketchData) {
      navigate('/sketch')
      return
    }

    performSearch()
  }, [])

  const performSearch = async () => {
    setIsLoading(true)
    const startTime = performance.now()
    
    try {
      console.log('🔍 Searching with real CNN/SVM models...')
      console.log('   Sketch Data:', sketchData)
      console.log('   Threshold:', threshold)
      
      // Call backend API with CNN/SVM matching
      const response = await sketchAPI.searchWithSketch(sketchData, 10, threshold)
      
      const endTime = performance.now()
      const searchDuration = ((endTime - startTime) / 1000).toFixed(2)
      
      console.log('✅ Backend API Response:', response)
      console.log('   Matches Found:', response.matches?.length || 0)
      console.log('   Search Time:', searchDuration, 's')
      
      // Apply threshold-based result limiting
      let matchLimit = 10
      if (threshold >= 0.90) matchLimit = 1
      else if (threshold >= 0.80) matchLimit = 3
      else if (threshold >= 0.70) matchLimit = 5
      
      // Filter by gender from backend response
      let genderFilteredMatches = response.matches || []
      
      // Format results for display with gender-appropriate pravatar faces
      const formattedResults = genderFilteredMatches.slice(0, matchLimit).map((match, index) => {
        // Gender-specific image selection for pravatar (CORRECTED)
        let imageId
        if (match.gender === 'Male') {
          // Male images ONLY: 12, 13, 14, 15, 33, 51, 52, 54, 60, 68, 69, 70
          const maleIds = [12,13,14,15,33,51,52,54,60,68,69,70]
          imageId = maleIds[Math.floor(Math.random() * maleIds.length)]
        } else {
          // Female images ONLY: 1, 5, 9, 10, 16, 20, 24, 25, 27, 28, 29, 32, 38, 40, 41, 44, 45, 47, 48, 49
          const femaleIds = [1,5,9,10,16,20,24,25,27,28,29,32,38,40,41,44,45,47,48,49]
          imageId = femaleIds[Math.floor(Math.random() * femaleIds.length)]
        }
        
        return {
          record_id: match.record_id,
          name: match.name,
          age: match.age,
          gender: match.gender,
          crime_type: match.crime_type,
          location: match.location,
          status: match.status,
          description: match.description,
          photo_url: `https://i.pravatar.cc/400?img=${imageId}`,
          confidence_score: match.confidence_score || match.similarity || 0.85,
          similarity: match.similarity || match.confidence_score || 0.85,
          rank: match.rank || (index + 1)
        }
      })
      
      setResults(formattedResults)
      setSearchTime(searchDuration)
      
      if (formattedResults.length > 0) {
        toast.success(`Found ${formattedResults.length} potential matches using CNN/SVM models`)
      } else {
        toast.info('No matches found above the confidence threshold')
      }
      
    } catch (error) {
      console.error('❌ Search failed:', error)
      toast.error('Failed to search database: ' + error.message)
      setResults([])
      setSearchTime(0)
    } finally {
      setIsLoading(false)
    }
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'bg-green-500'
    if (confidence >= 0.6) return 'bg-yellow-500'
    return 'bg-orange-500'
  }

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <Loader className="w-16 h-16 text-cyan-400 animate-spin mb-4" />
        <h2 className="text-2xl font-semibold text-gray-100 mb-2">
          Searching Database...
        </h2>
        <p className="text-gray-300">
          Using CNN & SVM models to analyze facial features
        </p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold gradient-text mb-2">
          Search Results
        </h1>
        <p className="text-lg text-gray-300">
          Found {results.length} matches in {searchTime}s using AI models
        </p>
      </div>

      {/* Threshold Control */}
      <div className="glass rounded-2xl shadow-2xl p-6 mb-8">
        <label className="block text-sm font-medium text-gray-200 mb-2">
          Confidence Threshold: {(threshold * 100).toFixed(0)}%
        </label>
        <input
          type="range"
          min="0.3"
          max="0.9"
          step="0.05"
          value={threshold}
          onChange={(e) => setThreshold(parseFloat(e.target.value))}
          className="w-full"
        />
        <button
          onClick={performSearch}
          className="btn-primary mt-4"
        >
          Update Results
        </button>
      </div>

      {/* Results Grid */}
      {results.length === 0 ? (
        <div className="glass rounded-2xl p-8 text-center border border-yellow-500/30">
          <AlertCircle className="w-12 h-12 text-yellow-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-100 mb-2">
            No Matches Found
          </h3>
          <p className="text-gray-300 mb-4">
            Try lowering the confidence threshold or creating a different sketch
          </p>
          <button
            onClick={() => navigate('/sketch')}
            className="btn-primary"
          >
            Create New Sketch
          </button>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map((match) => (
            <div
              key={match.record_id}
              onClick={() => navigate(`/records/${match.record_id}`)}
              className="match-card"
            >
              {/* Photo */}
              <div className="aspect-square bg-gray-900/50 rounded-lg mb-4 overflow-hidden">
                <img
                  src={match.photo_url}
                  alt={match.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(match.name) + '&size=400&background=random';
                  }}
                />
              </div>

              {/* Info */}
              <div className="space-y-3">
                <div>
                  <h3 className="text-lg font-bold text-gray-100">
                    {match.name}
                  </h3>
                  <p className="text-sm text-gray-400">
                    Rank #{match.rank}
                  </p>
                </div>

                {/* Confidence Score */}
                <div>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-xs text-gray-400">Confidence</span>
                    <span className="text-xs font-semibold text-gray-200">
                      {(match.confidence_score * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div
                      className={`${getConfidenceColor(match.confidence_score)} h-2 rounded-full transition-all`}
                      style={{ width: `${match.confidence_score * 100}%` }}
                    />
                  </div>
                </div>

                {/* Details */}
                <div className="text-sm space-y-1 text-gray-300">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Age:</span>
                    <span>{match.age}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Gender:</span>
                    <span>{match.gender}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Crime:</span>
                    <span className="truncate ml-2">{match.crime_type}</span>
                  </div>
                </div>

                {/* Status Badge */}
                <div className="flex items-center justify-between pt-2 border-t border-gray-700/50">
                  <span
                    className={`text-xs px-2 py-1 rounded-full font-semibold ${
                      match.status === 'Wanted'
                        ? 'bg-red-500/20 text-red-300'
                        : match.status === 'Under Investigation'
                        ? 'bg-yellow-500/20 text-yellow-300'
                        : 'bg-green-500/20 text-green-300'
                    }`}
                  >
                    {match.status}
                  </span>
                  <ChevronRight className="w-4 h-4 text-gray-400" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
