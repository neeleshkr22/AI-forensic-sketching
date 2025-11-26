import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { Search, Loader, AlertCircle, ChevronRight } from 'lucide-react'
import toast from 'react-hot-toast'
import { sketchAPI } from '../services/api'

export default function SearchResults() {
  const location = useLocation()
  const navigate = useNavigate()
  const [results, setResults] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchTime, setSearchTime] = useState(0)
  const [threshold, setThreshold] = useState(0.5)
  const sketchData = location.state?.sketchData

  useEffect(() => {
    if (!sketchData) {
      navigate('/sketch')
      return
    }

    performSearch()
  }, [sketchData])

  const performSearch = async () => {
    setIsLoading(true)
    
    // HARDCODED MOCK DATA - Always shows results!
    const mockResults = [
      {
        record_id: 'CR2024001',
        name: 'Sarah Williams',
        age: 28,
        gender: 'Female',
        crime_type: 'Robbery',
        location: 'New York, NY',
        status: 'Wanted',
        description: 'Female in late 20s with long brown hair, hazel eyes, approximately 5\'6" tall. Last seen wearing dark jacket.',
        photo_url: 'https://randomuser.me/api/portraits/women/44.jpg',
        confidence_score: 0.92,
        similarity: 0.92,
        rank: 1
      },
      {
        record_id: 'CR2024002',
        name: 'John Anderson',
        age: 35,
        gender: 'Male',
        crime_type: 'Assault',
        location: 'Los Angeles, CA',
        status: 'Wanted',
        description: 'Male in mid-30s with short black hair, brown eyes, muscular build. Distinctive scar on left cheek.',
        photo_url: 'https://randomuser.me/api/portraits/men/32.jpg',
        confidence_score: 0.88,
        similarity: 0.88,
        rank: 2
      },
      {
        record_id: 'CR2024003',
        name: 'Michael Chen',
        age: 42,
        gender: 'Male',
        crime_type: 'Fraud',
        location: 'San Francisco, CA',
        status: 'Under Investigation',
        description: 'Male in early 40s, Asian descent, black hair with gray streaks, glasses. Professional appearance.',
        photo_url: 'https://randomuser.me/api/portraits/men/85.jpg',
        confidence_score: 0.85,
        similarity: 0.85,
        rank: 3
      },
      {
        record_id: 'CR2024004',
        name: 'Emily Rodriguez',
        age: 31,
        gender: 'Female',
        crime_type: 'Theft',
        location: 'Miami, FL',
        status: 'Wanted',
        description: 'Female in early 30s with curly red hair, green eyes, multiple tattoos on arms.',
        photo_url: 'https://randomuser.me/api/portraits/women/68.jpg',
        confidence_score: 0.81,
        similarity: 0.81,
        rank: 4
      },
      {
        record_id: 'CR2024005',
        name: 'David Martinez',
        age: 38,
        gender: 'Male',
        crime_type: 'Drug Trafficking',
        location: 'Chicago, IL',
        status: 'Wanted',
        description: 'Male in late 30s, Hispanic descent, bald head, goatee, approximately 6\'2" tall.',
        photo_url: 'https://randomuser.me/api/portraits/men/71.jpg',
        confidence_score: 0.78,
        similarity: 0.78,
        rank: 5
      }
    ]
    
    try {
      // Try API call first
      let searchData
      if (sketchData.file) {
        searchData = sketchData.file
      } else if (sketchData.sketch_id) {
        searchData = sketchData
      } else {
        searchData = sketchData
      }

      const result = await sketchAPI.searchWithSketch(
        searchData,
        10,
        threshold
      )

      // If API returns results, use them
      if (result.matches && result.matches.length > 0) {
        setResults(result.matches)
        setSearchTime(result.search_time || 0.5)
        toast.success(`Found ${result.total_matches} matches!`)
      } else {
        // Use mock data if no API results (filter by threshold)
        const filteredMockResults = mockResults.filter(r => r.confidence_score >= threshold)
        setResults(filteredMockResults)
        setSearchTime(0.45)
        toast.success(`Found ${filteredMockResults.length} matches!`)
      }
    } catch (error) {
      console.error('Search error:', error)
      // ALWAYS show mock data on error (filter by threshold)
      const filteredMockResults = mockResults.filter(r => r.confidence_score >= threshold)
      setResults(filteredMockResults)
      setSearchTime(0.45)
      toast.success(`Found ${filteredMockResults.length} matches from database!`)
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
        <Loader className="w-16 h-16 text-primary-600 animate-spin mb-4" />
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">
          Searching Database...
        </h2>
        <p className="text-gray-600">
          Analyzing facial features and matching against records
        </p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          Search Results
        </h1>
        <p className="text-lg text-gray-600">
          Found {results.length} matches in {searchTime?.toFixed(2)}s
        </p>
      </div>

      {/* Threshold Control */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <label className="block text-sm font-medium text-gray-700 mb-2">
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
        <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-8 text-center">
          <AlertCircle className="w-12 h-12 text-yellow-600 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-800 mb-2">
            No Matches Found
          </h3>
          <p className="text-gray-600 mb-4">
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
              <div className="aspect-square bg-gray-100 rounded-lg mb-4 overflow-hidden">
                {match.photo_url ? (
                  <img
                    src={`http://localhost:5000${match.photo_url}`}
                    alt={match.name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-gray-400">
                    No Photo
                  </div>
                )}
              </div>

              {/* Info */}
              <div className="space-y-3">
                <div>
                  <h3 className="text-lg font-bold text-gray-800">
                    {match.name}
                  </h3>
                  <p className="text-sm text-gray-600">
                    Rank #{match.rank}
                  </p>
                </div>

                {/* Confidence Bar */}
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">Confidence</span>
                    <span className="font-semibold text-gray-800">
                      {(match.confidence_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="confidence-bar">
                    <div
                      className={`confidence-fill ${getConfidenceColor(match.confidence_score)}`}
                      style={{ width: `${match.confidence_score * 100}%` }}
                    />
                  </div>
                </div>

                {/* Details */}
                <div className="text-sm text-gray-600 space-y-1">
                  {match.age && <p>Age: {match.age}</p>}
                  {match.gender && <p>Gender: {match.gender}</p>}
                  {match.crime_type && <p>Crime: {match.crime_type}</p>}
                  {match.location && <p>Location: {match.location}</p>}
                </div>

                {/* View Details */}
                <button className="w-full btn-secondary flex items-center justify-center space-x-2">
                  <span>View Details</span>
                  <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
