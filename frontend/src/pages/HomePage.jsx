import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Sparkles, Upload, Palette } from 'lucide-react'
import toast from 'react-hot-toast'

export default function HomePage() {
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)

  const features = [
    {
      icon: Palette,
      title: 'Drag & Drop Composer',
      description: 'Build sketches by combining facial features like eyes, nose, mouth, and hair',
      action: () => navigate('/sketch?mode=manual'),
    },
    {
      icon: Sparkles,
      title: 'AI Generation',
      description: 'Generate sketches from text descriptions using advanced AI models',
      action: () => navigate('/sketch?mode=ai'),
    },
    {
      icon: Upload,
      title: 'Upload & Search',
      description: 'Upload an existing sketch and search the criminal database',
      action: () => navigate('/sketch?mode=upload'),
    },
  ]

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-16 gradient-bg text-white rounded-2xl">
        <h1 className="text-5xl font-bold mb-6">
          AI-Powered Criminal Sketch Matching
        </h1>
        <p className="text-xl mb-8 max-w-3xl mx-auto">
          Create accurate criminal sketches using drag-and-drop or AI generation,
          then instantly search our database using advanced deep learning models
        </p>
        <button
          onClick={() => navigate('/sketch')}
          className="bg-white text-primary-700 font-bold px-8 py-4 rounded-lg text-lg hover:bg-gray-100 transition-colors"
        >
          Get Started
        </button>
      </section>

      {/* Features Grid */}
      <section>
        <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">
          How It Works
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          {features.map(({ icon: Icon, title, description, action }, index) => (
            <div
              key={index}
              onClick={action}
              className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow cursor-pointer group"
            >
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center group-hover:bg-primary-200 transition-colors">
                  <Icon className="w-8 h-8 text-primary-600" />
                </div>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-3 text-center">
                {title}
              </h3>
              <p className="text-gray-600 text-center">
                {description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Technology Stack */}
      <section className="bg-white rounded-xl p-8 shadow-lg">
        <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">
          Powered by Advanced AI
        </h2>
        <div className="grid md:grid-cols-4 gap-6 text-center">
          <div>
            <h4 className="font-bold text-lg text-primary-600 mb-2">CNN</h4>
            <p className="text-sm text-gray-600">
              Deep learning feature extraction using FaceNet
            </p>
          </div>
          <div>
            <h4 className="font-bold text-lg text-primary-600 mb-2">SVM</h4>
            <p className="text-sm text-gray-600">
              Support Vector Machine for accurate matching
            </p>
          </div>
          <div>
            <h4 className="font-bold text-lg text-primary-600 mb-2">GAN</h4>
            <p className="text-sm text-gray-600">
              Generative model for sketch enhancement
            </p>
          </div>
          <div>
            <h4 className="font-bold text-lg text-primary-600 mb-2">OpenCV</h4>
            <p className="text-sm text-gray-600">
              Image processing and face detection
            </p>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="grid md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-8 rounded-xl text-center">
          <h3 className="text-4xl font-bold mb-2">85-90%</h3>
          <p className="text-lg">Matching Accuracy</p>
        </div>
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white p-8 rounded-xl text-center">
          <h3 className="text-4xl font-bold mb-2">&lt;2s</h3>
          <p className="text-lg">Search Speed</p>
        </div>
        <div className="bg-gradient-to-br from-pink-500 to-pink-600 text-white p-8 rounded-xl text-center">
          <h3 className="text-4xl font-bold mb-2">512D</h3>
          <p className="text-lg">Feature Vectors</p>
        </div>
      </section>
    </div>
  )
}
