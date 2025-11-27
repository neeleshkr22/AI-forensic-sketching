import { useState } from 'react'
import { Wand2, Loader } from 'lucide-react'
import toast from 'react-hot-toast'
import { sketchAPI } from '../services/api'

export default function AISketchGenerator({ onComplete }) {
  const [prompt, setPrompt] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedSketch, setGeneratedSketch] = useState(null)

  const examplePrompts = [
    'Male, 30s, short black hair, brown eyes, round face, beard',
    'Female, 20s, long blonde hair, blue eyes, oval face',
    'Male, 40s, bald, green eyes, square jaw, scar on left cheek',
    'Female, 50s, curly red hair, glasses, freckles',
  ]

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast.error('Please enter a description')
      return
    }

    setIsGenerating(true)
    try {
      const result = await sketchAPI.generateFromPrompt(prompt)
      setGeneratedSketch(result)
      onComplete(result)
      toast.success('Sketch generated successfully!')
    } catch (error) {
      toast.error('Generation failed: ' + error.message)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-semibold text-gray-100 mb-4">
          Describe the Person
        </h3>
        <p className="text-gray-300 mb-4">
          Provide a detailed description of facial features, age, gender, hair color, etc.
        </p>

        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="E.g., Male in his 30s with short black hair, brown eyes, round face, and a beard..."
          className="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none resize-none"
        />
      </div>

      {/* Example Prompts */}
      <div>
        <p className="text-sm text-gray-300 mb-2">Quick examples:</p>
        <div className="flex flex-wrap gap-2">
          {examplePrompts.map((example, index) => (
            <button
              key={index}
              onClick={() => setPrompt(example)}
              className="text-sm px-3 py-1 glass glass-hover rounded-full text-gray-200 transition-colors"
            >
              {example.substring(0, 30)}...
            </button>
          ))}
        </div>
      </div>

      {/* Generate Button */}
      <button
        onClick={handleGenerate}
        disabled={isGenerating || !prompt.trim()}
        className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isGenerating ? (
          <>
            <Loader className="w-5 h-5 animate-spin" />
            <span>Generating...</span>
          </>
        ) : (
          <>
            <Wand2 className="w-5 h-5" />
            <span>Generate Sketch</span>
          </>
        )}
      </button>

      {/* Generated Sketch Preview */}
      {generatedSketch && (
        <div className="glass rounded-2xl p-4">
          <h4 className="font-semibold text-gray-100 mb-3">Generated Sketch</h4>
          <div className="bg-gray-900/50 rounded-lg p-4 flex items-center justify-center">
            <img
              src={sketchAPI.getSketchImage(generatedSketch.sketch_id)}
              alt="Generated sketch"
              className="max-w-full h-auto rounded-lg shadow-md"
            />
          </div>
          <p className="text-sm text-gray-600 mt-3">
            <strong>Prompt:</strong> {generatedSketch.prompt}
          </p>
        </div>
      )}
    </div>
  )
}
