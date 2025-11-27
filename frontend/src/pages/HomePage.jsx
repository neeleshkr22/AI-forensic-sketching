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
      <section className="text-center py-16 bg-gradient-to-br from-cyan-600 via-blue-600 to-teal-600 text-white rounded-2xl shadow-2xl shadow-cyan-500/20">
        <h1 className="text-5xl font-bold mb-6">
          AI-Powered Criminal Sketch Matching
        </h1>
        <p className="text-xl mb-8 max-w-3xl mx-auto">
          Create accurate criminal sketches using drag-and-drop or AI generation,
          then instantly search our database using advanced deep learning models
        </p>
        <button
          onClick={() => navigate('/sketch')}
          className="bg-white text-cyan-700 font-bold px-8 py-4 rounded-xl text-lg hover:bg-gray-100 transition-all transform hover:scale-105 hover:-translate-y-0.5 shadow-xl"
        >
          Get Started
        </button>
      </section>

      {/* Features Grid */}
      <section>
        <h2 className="text-3xl font-bold gradient-text mb-8 text-center">
          How It Works
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          {features.map(({ icon: Icon, title, description, action }, index) => (
            <div
              key={index}
              onClick={action}
              className="glass glass-hover p-8 rounded-2xl shadow-2xl cursor-pointer group hover:scale-[1.02] hover:-translate-y-1 transition-all duration-300"
            >
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 rounded-full flex items-center justify-center group-hover:from-cyan-500/30 group-hover:to-blue-500/30 transition-colors border border-cyan-400/30">
                  <Icon className="w-8 h-8 text-cyan-400" />
                </div>
              </div>
              <h3 className="text-xl font-bold text-gray-100 mb-3 text-center">
                {title}
              </h3>
              <p className="text-gray-300 text-center">
                {description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* Technology Stack */}
      <section className="glass rounded-2xl p-8 shadow-2xl">
        <h2 className="text-3xl font-bold gradient-text mb-6 text-center">
          Powered by Advanced AI
        </h2>
        <div className="grid md:grid-cols-4 gap-6 text-center">
          <div>
            <h4 className="font-bold text-lg text-cyan-400 mb-2">CNN</h4>
            <p className="text-sm text-gray-300">
              Deep learning feature extraction using FaceNet
            </p>
          </div>
          <div>
            <h4 className="font-bold text-lg text-blue-400 mb-2">SVM</h4>
            <p className="text-sm text-gray-300">
              Support Vector Machine for accurate matching
            </p>
          </div>
          <div>
            <h4 className="font-bold text-lg text-teal-400 mb-2">GAN</h4>
            <p className="text-sm text-gray-300">
              Generative model for sketch enhancement
            </p>
          </div>
          <div>
            <h4 className="font-bold text-lg text-cyan-400 mb-2">OpenCV</h4>
            <p className="text-sm text-gray-300">
              Image processing and face detection
            </p>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="grid md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-cyan-600 to-cyan-700 text-white p-8 rounded-2xl text-center shadow-2xl shadow-cyan-500/20 hover:scale-105 transition-transform duration-300">
          <h3 className="text-4xl font-bold mb-2">85-90%</h3>
          <p className="text-lg">Matching Accuracy</p>
        </div>
        <div className="bg-gradient-to-br from-blue-600 to-blue-700 text-white p-8 rounded-2xl text-center shadow-2xl shadow-blue-500/20 hover:scale-105 transition-transform duration-300">
          <h3 className="text-4xl font-bold mb-2">&lt;2s</h3>
          <p className="text-lg">Search Speed</p>
        </div>
        <div className="bg-gradient-to-br from-teal-600 to-teal-700 text-white p-8 rounded-2xl text-center shadow-2xl shadow-teal-500/20 hover:scale-105 transition-transform duration-300">
          <h3 className="text-4xl font-bold mb-2">512D</h3>
          <p className="text-lg">Feature Vectors</p>
        </div>
      </section>
    </div>
  )
}
