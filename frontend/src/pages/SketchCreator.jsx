import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { Sparkles, Palette, Upload, Search } from 'lucide-react'
import toast from 'react-hot-toast'
import AISketchGenerator from '../components/AISketchGenerator'
import ManualSketchComposer from '../components/ManualSketchComposer'
import SketchUploader from '../components/SketchUploader'

export default function SketchCreator() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [mode, setMode] = useState(searchParams.get('mode') || 'ai')
  const [sketchData, setSketchData] = useState(null)
  const [isSearching, setIsSearching] = useState(false)

  const modes = [
    { id: 'ai', label: 'AI Generation', icon: Sparkles },
    { id: 'manual', label: 'Drag & Drop', icon: Palette },
    { id: 'upload', label: 'Upload', icon: Upload },
  ]

  const handleSketchComplete = (data) => {
    setSketchData(data)
    toast.success('Sketch created successfully!')
  }

  const handleSearch = async () => {
    if (!sketchData) {
      toast.error('Please create or upload a sketch first')
      return
    }

    setIsSearching(true)
    try {
      // Navigate to results page with sketch data
      navigate('/results', { state: { sketchData } })
    } catch (error) {
      toast.error('Search failed: ' + error.message)
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Create Criminal Sketch
        </h1>
        <p className="text-lg text-gray-600">
          Choose your preferred method to create a sketch
        </p>
      </div>

      {/* Mode Selector */}
      <div className="flex space-x-4 mb-8">
        {modes.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setMode(id)}
            className={`flex items-center space-x-2 px-6 py-3 rounded-lg font-medium transition-all ${
              mode === id
                ? 'bg-primary-600 text-white shadow-lg'
                : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            <Icon className="w-5 h-5" />
            <span>{label}</span>
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
        {mode === 'ai' && <AISketchGenerator onComplete={handleSketchComplete} />}
        {mode === 'manual' && <ManualSketchComposer onComplete={handleSketchComplete} />}
        {mode === 'upload' && <SketchUploader onComplete={handleSketchComplete} />}
      </div>

      {/* Action Buttons */}
      {sketchData && (
        <div className="flex justify-end space-x-4">
          <button
            onClick={() => setSketchData(null)}
            className="btn-secondary"
          >
            Clear
          </button>
          <button
            onClick={handleSearch}
            disabled={isSearching}
            className="btn-primary flex items-center space-x-2"
          >
            <Search className="w-5 h-5" />
            <span>{isSearching ? 'Searching...' : 'Search Database'}</span>
          </button>
        </div>
      )}
    </div>
  )
}
