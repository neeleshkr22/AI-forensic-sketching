import { useState, useRef, useEffect, useCallback } from 'react'
import { Stage, Layer, Image as KonvaImage, Transformer, Line, Rect } from 'react-konva'
import { 
  Download, Trash2, Undo, Redo, Layers, 
  FlipHorizontal, FlipVertical, Copy, Grid3x3,
  Eye, EyeOff, Lock, Unlock, Move, Pencil, Eraser,
  ChevronUp, ChevronDown, Maximize, Minimize
} from 'lucide-react'
import toast from 'react-hot-toast'

// Facial components with actual images
const facialComponents = {
  face: [
    { id: 'face1', name: 'Oval Face', url: '/assets/face-parts/face1.png', category: 'face' },
    { id: 'face2', name: 'Round Face', url: '/assets/face-parts/face2.png', category: 'face' },
    { id: 'face3', name: 'Square Face', url: '/assets/face-parts/face3.png', category: 'face' },
    { id: 'face4', name: 'Long Face', url: '/assets/face-parts/face4.png', category: 'face' },
  ],
  eyes: [
    { id: 'eyes1', name: 'Round Eyes', url: '/assets/face-parts/eye1.png', category: 'eyes' },
    { id: 'eyes2', name: 'Almond Eyes', url: '/assets/face-parts/eye2.png', category: 'eyes' },
    { id: 'eyes3', name: 'Narrow Eyes', url: '/assets/face-parts/eye3.png', category: 'eyes' },
    { id: 'eyes4', name: 'Wide Eyes', url: '/assets/face-parts/eye4.png', category: 'eyes' },
  ],
  nose: [
    { id: 'nose1', name: 'Straight Nose', url: '/assets/face-parts/nose1.png', category: 'nose' },
    { id: 'nose2', name: 'Button Nose', url: '/assets/face-parts/nose2.png', category: 'nose' },
    { id: 'nose3', name: 'Hook Nose', url: '/assets/face-parts/nose3.png', category: 'nose' },
    { id: 'nose4', name: 'Broad Nose', url: '/assets/face-parts/nose4.png', category: 'nose' },
  ],
  mouth: [
    { id: 'mouth1', name: 'Thin Lips', url: '/assets/face-parts/mouth1.png', category: 'mouth' },
    { id: 'mouth2', name: 'Full Lips', url: '/assets/face-parts/mouth2.png', category: 'mouth' },
    { id: 'mouth3', name: 'Wide Mouth', url: '/assets/face-parts/mouth3.png', category: 'mouth' },
    { id: 'mouth4', name: 'Small Mouth', url: '/assets/face-parts/mouth4.png', category: 'mouth' },
  ],
  hair: [
    { id: 'hair1', name: 'Short Hair', url: '/assets/face-parts/hair1.png', category: 'hair' },
    { id: 'hair2', name: 'Long Hair', url: '/assets/face-parts/hair2.png', category: 'hair' },
    { id: 'hair3', name: 'Curly Hair', url: '/assets/face-parts/hair3.png', category: 'hair' },
    { id: 'hair4', name: 'Bald', url: '/assets/face-parts/hair4.png', category: 'hair' },
  ],
}

export default function ManualSketchComposer({ onComplete }) {
  const [selectedCategory, setSelectedCategory] = useState('face')
  const [placedComponents, setPlacedComponents] = useState([])
  const [selectedId, setSelectedId] = useState(null)
  const [history, setHistory] = useState([])
  const [historyStep, setHistoryStep] = useState(0)
  const [tool, setTool] = useState('select') // 'select', 'draw', 'erase'
  const [brushSize, setBrushSize] = useState(2)
  const [isDrawing, setIsDrawing] = useState(false)
  const [lines, setLines] = useState([])
  const [showGrid, setShowGrid] = useState(false)
  const [zoom, setZoom] = useState(1)
  const [showLayers, setShowLayers] = useState(true)
  const stageRef = useRef(null)
  const layerRef = useRef(null)

  // Save state to history
  const saveHistory = useCallback(() => {
    const newHistory = history.slice(0, historyStep + 1)
    newHistory.push({ components: [...placedComponents], lines: [...lines] })
    setHistory(newHistory)
    setHistoryStep(newHistory.length - 1)
  }, [history, historyStep, placedComponents, lines])

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.ctrlKey && e.key === 'z') {
        e.preventDefault()
        handleUndo()
      } else if (e.ctrlKey && e.key === 'y') {
        e.preventDefault()
        handleRedo()
      } else if (e.key === 'Delete' && selectedId) {
        handleDelete()
      } else if (e.ctrlKey && e.key === 'd' && selectedId) {
        e.preventDefault()
        handleDuplicate()
      }
    }
    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [selectedId, placedComponents, historyStep])

  const handleComponentClick = (component) => {
    const newComponent = {
      id: `${component.id}_${Date.now()}`,
      name: component.name,
      category: component.category,
      imageUrl: component.url,
      x: 300 - 50,
      y: 300 - 50,
      width: 100,
      height: 100,
      scaleX: 1,
      scaleY: 1,
      rotation: 0,
      opacity: 1,
      visible: true,
      locked: false,
      zIndex: placedComponents.length,
    }
    setPlacedComponents([...placedComponents, newComponent])
    setSelectedId(newComponent.id)
    saveHistory()
    toast.success(`${component.name} added`)
  }

  const handleTransform = (id, attrs) => {
    setPlacedComponents(
      placedComponents.map((comp) =>
        comp.id === id ? { ...comp, ...attrs } : comp
      )
    )
  }

  const handleDelete = () => {
    if (selectedId) {
      setPlacedComponents(placedComponents.filter((c) => c.id !== selectedId))
      setSelectedId(null)
      saveHistory()
      toast.success('Component removed')
    }
  }

  const handleDuplicate = () => {
    if (selectedId) {
      const comp = placedComponents.find(c => c.id === selectedId)
      if (comp) {
        const newComp = { 
          ...comp, 
          id: `${comp.category}_${Date.now()}`,
          x: comp.x + 20, 
          y: comp.y + 20,
          zIndex: placedComponents.length
        }
        setPlacedComponents([...placedComponents, newComp])
        setSelectedId(newComp.id)
        saveHistory()
        toast.success('Component duplicated')
      }
    }
  }

  const handleFlipH = () => {
    if (selectedId) {
      setPlacedComponents(
        placedComponents.map((comp) =>
          comp.id === selectedId ? { ...comp, scaleX: -comp.scaleX } : comp
        )
      )
      saveHistory()
    }
  }

  const handleFlipV = () => {
    if (selectedId) {
      setPlacedComponents(
        placedComponents.map((comp) =>
          comp.id === selectedId ? { ...comp, scaleY: -comp.scaleY } : comp
        )
      )
      saveHistory()
    }
  }

  const handleLayerMove = (id, direction) => {
    const index = placedComponents.findIndex(c => c.id === id)
    if (index === -1) return
    
    const newComponents = [...placedComponents]
    const newIndex = direction === 'up' ? Math.min(index + 1, newComponents.length - 1) : Math.max(index - 1, 0)
    
    [newComponents[index], newComponents[newIndex]] = [newComponents[newIndex], newComponents[index]]
    setPlacedComponents(newComponents)
    saveHistory()
  }

  const handleToggleVisibility = (id) => {
    setPlacedComponents(
      placedComponents.map((comp) =>
        comp.id === id ? { ...comp, visible: !comp.visible } : comp
      )
    )
  }

  const handleToggleLock = (id) => {
    setPlacedComponents(
      placedComponents.map((comp) =>
        comp.id === id ? { ...comp, locked: !comp.locked } : comp
      )
    )
  }

  const handleUndo = () => {
    if (historyStep > 0) {
      const newStep = historyStep - 1
      setHistoryStep(newStep)
      setPlacedComponents(history[newStep].components)
      setLines(history[newStep].lines)
    }
  }

  const handleRedo = () => {
    if (historyStep < history.length - 1) {
      const newStep = historyStep + 1
      setHistoryStep(newStep)
      setPlacedComponents(history[newStep].components)
      setLines(history[newStep].lines)
    }
  }

  const handleMouseDown = (e) => {
    if (tool !== 'select' && tool !== 'move') {
      setIsDrawing(true)
      const pos = e.target.getStage().getPointerPosition()
      setLines([...lines, { 
        tool, 
        points: [pos.x, pos.y],
        brushSize,
        color: tool === 'draw' ? '#000000' : '#FFFFFF'
      }])
    }
  }

  const handleMouseMove = (e) => {
    if (!isDrawing) return
    
    const stage = e.target.getStage()
    const point = stage.getPointerPosition()
    
    let lastLine = lines[lines.length - 1]
    lastLine.points = lastLine.points.concat([point.x, point.y])
    
    lines.splice(lines.length - 1, 1, lastLine)
    setLines(lines.concat())
  }

  const handleMouseUp = () => {
    if (isDrawing) {
      setIsDrawing(false)
      saveHistory()
    }
  }

  const handleSave = () => {
    if (placedComponents.length === 0 && lines.length === 0) {
      toast.error('Please add some components or draw something first')
      return
    }

    // Deselect before export
    setSelectedId(null)
    
    setTimeout(() => {
      const stage = stageRef.current
      const dataURL = stage.toDataURL({ 
        pixelRatio: 2, // Higher quality
        mimeType: 'image/png'
      })

      fetch(dataURL)
        .then((res) => res.blob())
        .then((blob) => {
          const file = new File([blob], 'sketch.png', { type: 'image/png' })
          onComplete({ file, components: placedComponents, lines })
          toast.success('Sketch saved successfully!')
        })
    }, 100)
  }

  const handleClearCanvas = () => {
    if (window.confirm('Clear entire canvas? This cannot be undone.')) {
      setPlacedComponents([])
      setLines([])
      setSelectedId(null)
      saveHistory()
      toast.success('Canvas cleared')
    }
  }

  const selectedComponent = placedComponents.find(c => c.id === selectedId)

  return (
    <div className="flex h-full gap-4">
      {/* Left Sidebar - Component Library */}
      <div className="w-64 bg-white rounded-lg shadow-lg p-4 overflow-y-auto" style={{ maxHeight: '800px' }}>
        <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
          <Layers className="w-5 h-5 mr-2" />
          Components
        </h3>

        {/* Category Tabs */}
        <div className="space-y-1 mb-4">
          {Object.keys(facialComponents).map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`w-full text-left px-3 py-2 rounded-md capitalize transition-all text-sm font-medium ${
                selectedCategory === category
                  ? 'bg-primary-600 text-white shadow-sm'
                  : 'bg-gray-50 text-gray-700 hover:bg-gray-100'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Component Items */}
        <div className="space-y-2">
          {facialComponents[selectedCategory].map((component) => (
            <div
              key={component.id}
              onClick={() => handleComponentClick(component)}
              className="bg-gradient-to-br from-gray-50 to-gray-100 border border-gray-200 rounded-lg p-2 cursor-pointer hover:border-primary-400 hover:shadow-md transition-all group"
            >
              <div className="aspect-square bg-white rounded-md mb-2 flex items-center justify-center overflow-hidden shadow-sm">
                <img 
                  src={component.url} 
                  alt={component.name}
                  className="w-full h-full object-contain p-1 group-hover:scale-110 transition-transform"
                />
              </div>
              <p className="text-xs font-medium text-center text-gray-700">{component.name}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Center - Canvas Area */}
      <div className="flex-1 flex flex-col bg-white rounded-lg shadow-lg">
        {/* Toolbar */}
        <div className="border-b border-gray-200 p-3 bg-gray-50">
          <div className="flex items-center justify-between flex-wrap gap-2">
            {/* Tool Selection */}
            <div className="flex items-center space-x-1 bg-white rounded-lg p-1 shadow-sm">
              <button
                onClick={() => setTool('select')}
                className={`p-2 rounded-md transition-colors ${
                  tool === 'select' ? 'bg-primary-600 text-white' : 'text-gray-600 hover:bg-gray-100'
                }`}
                title="Select Tool (V)"
              >
                <Move className="w-4 h-4" />
              </button>
              <button
                onClick={() => setTool('draw')}
                className={`p-2 rounded-md transition-colors ${
                  tool === 'draw' ? 'bg-primary-600 text-white' : 'text-gray-600 hover:bg-gray-100'
                }`}
                title="Draw Tool (D)"
              >
                <Pencil className="w-4 h-4" />
              </button>
              <button
                onClick={() => setTool('erase')}
                className={`p-2 rounded-md transition-colors ${
                  tool === 'erase' ? 'bg-primary-600 text-white' : 'text-gray-600 hover:bg-gray-100'
                }`}
                title="Eraser Tool (E)"
              >
                <Eraser className="w-4 h-4" />
              </button>
            </div>

            {/* Brush Size */}
            {(tool === 'draw' || tool === 'erase') && (
              <div className="flex items-center space-x-2 bg-white rounded-lg px-3 py-1 shadow-sm">
                <span className="text-xs text-gray-600">Brush:</span>
                <input
                  type="range"
                  min="1"
                  max="20"
                  value={brushSize}
                  onChange={(e) => setBrushSize(Number(e.target.value))}
                  className="w-20"
                />
                <span className="text-xs font-medium text-gray-700 w-6">{brushSize}</span>
              </div>
            )}

            {/* Transformation Controls */}
            <div className="flex items-center space-x-1 bg-white rounded-lg p-1 shadow-sm">
              <button
                onClick={handleUndo}
                disabled={historyStep === 0}
                className="p-2 rounded-md text-gray-600 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
                title="Undo (Ctrl+Z)"
              >
                <Undo className="w-4 h-4" />
              </button>
              <button
                onClick={handleRedo}
                disabled={historyStep >= history.length - 1}
                className="p-2 rounded-md text-gray-600 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
                title="Redo (Ctrl+Y)"
              >
                <Redo className="w-4 h-4" />
              </button>
              <div className="w-px h-6 bg-gray-300 mx-1"></div>
              <button
                onClick={handleFlipH}
                disabled={!selectedId}
                className="p-2 rounded-md text-gray-600 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
                title="Flip Horizontal"
              >
                <FlipHorizontal className="w-4 h-4" />
              </button>
              <button
                onClick={handleFlipV}
                disabled={!selectedId}
                className="p-2 rounded-md text-gray-600 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
                title="Flip Vertical"
              >
                <FlipVertical className="w-4 h-4" />
              </button>
              <button
                onClick={handleDuplicate}
                disabled={!selectedId}
                className="p-2 rounded-md text-gray-600 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed"
                title="Duplicate (Ctrl+D)"
              >
                <Copy className="w-4 h-4" />
              </button>
              <button
                onClick={handleDelete}
                disabled={!selectedId}
                className="p-2 rounded-md text-red-600 hover:bg-red-50 disabled:opacity-30 disabled:cursor-not-allowed"
                title="Delete (Del)"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>

            {/* View Controls */}
            <div className="flex items-center space-x-1 bg-white rounded-lg p-1 shadow-sm">
              <button
                onClick={() => setShowGrid(!showGrid)}
                className={`p-2 rounded-md transition-colors ${
                  showGrid ? 'bg-primary-100 text-primary-600' : 'text-gray-600 hover:bg-gray-100'
                }`}
                title="Toggle Grid"
              >
                <Grid3x3 className="w-4 h-4" />
              </button>
              <button
                onClick={() => setZoom(Math.max(0.5, zoom - 0.1))}
                className="p-2 rounded-md text-gray-600 hover:bg-gray-100"
                title="Zoom Out"
              >
                <Minimize className="w-4 h-4" />
              </button>
              <span className="text-xs font-medium text-gray-700 px-2">{Math.round(zoom * 100)}%</span>
              <button
                onClick={() => setZoom(Math.min(2, zoom + 0.1))}
                className="p-2 rounded-md text-gray-600 hover:bg-gray-100"
                title="Zoom In"
              >
                <Maximize className="w-4 h-4" />
              </button>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center space-x-2">
              <button
                onClick={handleClearCanvas}
                className="px-3 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 text-sm font-medium"
              >
                Clear All
              </button>
              <button
                onClick={handleSave}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center space-x-2 text-sm font-medium shadow-sm"
              >
                <Download className="w-4 h-4" />
                <span>Export Sketch</span>
              </button>
            </div>
          </div>
        </div>

        {/* Canvas */}
        <div className="flex-1 p-4 bg-gradient-to-br from-gray-50 to-gray-100 overflow-auto">
          <div className="inline-block bg-white rounded-lg shadow-xl" style={{ 
            transform: `scale(${zoom})`, 
            transformOrigin: 'top left',
            border: '2px solid #e5e7eb'
          }}>
            <Stage
              ref={stageRef}
              width={700}
              height={700}
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              onClick={(e) => {
                if (tool === 'select' && e.target === e.target.getStage()) {
                  setSelectedId(null)
                }
              }}
            >
              <Layer ref={layerRef}>
                {/* Grid */}
                {showGrid && <GridLayer />}
                
                {/* Drawing Lines */}
                {lines.map((line, i) => (
                  <Line
                    key={i}
                    points={line.points}
                    stroke={line.color}
                    strokeWidth={line.brushSize}
                    tension={0.5}
                    lineCap="round"
                    lineJoin="round"
                    globalCompositeOperation={
                      line.tool === 'erase' ? 'destination-out' : 'source-over'
                    }
                  />
                ))}
                
                {/* Components */}
                {placedComponents
                  .filter(comp => comp.visible)
                  .map((comp) => (
                    <ComponentImage
                      key={comp.id}
                      component={comp}
                      isSelected={comp.id === selectedId && tool === 'select'}
                      onSelect={() => {
                        if (tool === 'select' && !comp.locked) {
                          setSelectedId(comp.id)
                        }
                      }}
                      onChange={(attrs) => handleTransform(comp.id, attrs)}
                      isDraggable={tool === 'select' && !comp.locked}
                    />
                  ))}
              </Layer>
            </Stage>
          </div>
        </div>
      </div>

      {/* Right Sidebar - Layers & Properties */}
      {showLayers && (
        <div className="w-72 bg-white rounded-lg shadow-lg p-4 overflow-y-auto" style={{ maxHeight: '800px' }}>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-gray-800 flex items-center">
              <Layers className="w-5 h-5 mr-2" />
              Layers
            </h3>
            <span className="text-xs text-gray-500">{placedComponents.length} items</span>
          </div>

          {/* Selected Component Properties */}
          {selectedComponent && (
            <div className="mb-4 p-3 bg-primary-50 rounded-lg border border-primary-200">
              <h4 className="text-sm font-semibold text-primary-900 mb-2">Properties</h4>
              <div className="space-y-2">
                <div>
                  <label className="text-xs text-gray-600">Name</label>
                  <p className="text-sm font-medium text-gray-800">{selectedComponent.name}</p>
                </div>
                <div>
                  <label className="text-xs text-gray-600">Opacity</label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={selectedComponent.opacity}
                    onChange={(e) => handleTransform(selectedId, { opacity: parseFloat(e.target.value) })}
                    className="w-full"
                  />
                  <span className="text-xs text-gray-600">{Math.round(selectedComponent.opacity * 100)}%</span>
                </div>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <label className="text-gray-600">X:</label>
                    <p className="font-mono text-gray-800">{Math.round(selectedComponent.x)}</p>
                  </div>
                  <div>
                    <label className="text-gray-600">Y:</label>
                    <p className="font-mono text-gray-800">{Math.round(selectedComponent.y)}</p>
                  </div>
                  <div>
                    <label className="text-gray-600">Rotation:</label>
                    <p className="font-mono text-gray-800">{Math.round(selectedComponent.rotation)}°</p>
                  </div>
                  <div>
                    <label className="text-gray-600">Scale:</label>
                    <p className="font-mono text-gray-800">{selectedComponent.scaleX.toFixed(2)}x</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Layer List */}
          <div className="space-y-1">
            {placedComponents.length === 0 ? (
              <p className="text-sm text-gray-400 text-center py-8">No components yet</p>
            ) : (
              [...placedComponents].reverse().map((comp, index) => (
                <div
                  key={comp.id}
                  onClick={() => !comp.locked && setSelectedId(comp.id)}
                  className={`p-2 rounded-lg cursor-pointer transition-all ${
                    comp.id === selectedId
                      ? 'bg-primary-100 border-2 border-primary-400'
                      : 'bg-gray-50 border-2 border-transparent hover:bg-gray-100'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2 flex-1 min-w-0">
                      <img 
                        src={comp.imageUrl} 
                        alt={comp.name}
                        className="w-8 h-8 object-contain bg-white rounded border"
                      />
                      <span className="text-sm font-medium text-gray-800 truncate">{comp.name}</span>
                    </div>
                    
                    <div className="flex items-center space-x-1">
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleLayerMove(comp.id, 'up')
                        }}
                        className="p-1 text-gray-400 hover:text-gray-600"
                        title="Move Up"
                      >
                        <ChevronUp className="w-3 h-3" />
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleLayerMove(comp.id, 'down')
                        }}
                        className="p-1 text-gray-400 hover:text-gray-600"
                        title="Move Down"
                      >
                        <ChevronDown className="w-3 h-3" />
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleToggleVisibility(comp.id)
                        }}
                        className="p-1 text-gray-400 hover:text-gray-600"
                        title={comp.visible ? 'Hide' : 'Show'}
                      >
                        {comp.visible ? <Eye className="w-3 h-3" /> : <EyeOff className="w-3 h-3" />}
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation()
                          handleToggleLock(comp.id)
                        }}
                        className="p-1 text-gray-400 hover:text-gray-600"
                        title={comp.locked ? 'Unlock' : 'Lock'}
                      >
                        {comp.locked ? <Lock className="w-3 h-3" /> : <Unlock className="w-3 h-3" />}
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Tips */}
          <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
            <h4 className="text-xs font-semibold text-blue-900 mb-2">💡 Shortcuts</h4>
            <ul className="text-xs text-blue-800 space-y-1">
              <li>• <kbd className="font-mono bg-white px-1 rounded">Ctrl+Z</kbd> Undo</li>
              <li>• <kbd className="font-mono bg-white px-1 rounded">Ctrl+Y</kbd> Redo</li>
              <li>• <kbd className="font-mono bg-white px-1 rounded">Ctrl+D</kbd> Duplicate</li>
              <li>• <kbd className="font-mono bg-white px-1 rounded">Delete</kbd> Remove</li>
              <li>• Drag corners to resize & rotate</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}

// Grid Component
function GridLayer() {
  const lines = []
  const gridSize = 50
  const width = 700
  const height = 700

  // Vertical lines
  for (let i = 0; i <= width / gridSize; i++) {
    lines.push(
      <Line
        key={`v${i}`}
        points={[i * gridSize, 0, i * gridSize, height]}
        stroke="#e0e0e0"
        strokeWidth={1}
      />
    )
  }

  // Horizontal lines
  for (let i = 0; i <= height / gridSize; i++) {
    lines.push(
      <Line
        key={`h${i}`}
        points={[0, i * gridSize, width, i * gridSize]}
        stroke="#e0e0e0"
        strokeWidth={1}
      />
    )
  }

  return <>{lines}</>
}

// Component for individual placed items
function ComponentImage({ component, isSelected, onSelect, onChange, isDraggable }) {
  const shapeRef = useRef()
  const trRef = useRef()
  const [image, setImage] = useState(null)

  // Load image
  useEffect(() => {
    const img = new window.Image()
    img.src = component.imageUrl
    img.onload = () => setImage(img)
    img.onerror = () => {
      console.error('Failed to load image:', component.imageUrl)
    }
  }, [component.imageUrl])

  // Attach transformer
  useEffect(() => {
    if (isSelected && trRef.current && shapeRef.current) {
      trRef.current.nodes([shapeRef.current])
      trRef.current.getLayer().batchDraw()
    }
  }, [isSelected])

  if (!image) return null

  return (
    <>
      <KonvaImage
        ref={shapeRef}
        image={image}
        x={component.x}
        y={component.y}
        width={component.width}
        height={component.height}
        scaleX={component.scaleX}
        scaleY={component.scaleY}
        rotation={component.rotation}
        opacity={component.opacity}
        draggable={isDraggable}
        onClick={onSelect}
        onTap={onSelect}
        onDragEnd={(e) => {
          onChange({
            x: e.target.x(),
            y: e.target.y(),
          })
        }}
        onTransformEnd={(e) => {
          const node = shapeRef.current
          const scaleX = node.scaleX()
          const scaleY = node.scaleY()
          
          // Reset scale to 1 and adjust width/height instead for better quality
          node.scaleX(1)
          node.scaleY(1)

          onChange({
            x: node.x(),
            y: node.y(),
            width: Math.max(5, node.width() * scaleX),
            height: Math.max(5, node.height() * scaleY),
            scaleX: scaleX,
            scaleY: scaleY,
            rotation: node.rotation(),
          })
        }}
        shadowColor="black"
        shadowBlur={isSelected ? 10 : 0}
        shadowOpacity={isSelected ? 0.3 : 0}
        shadowOffset={{ x: 0, y: 0 }}
      />
      {isSelected && (
        <Transformer
          ref={trRef}
          rotateEnabled={true}
          enabledAnchors={[
            'top-left',
            'top-right',
            'bottom-left',
            'bottom-right',
          ]}
          borderStroke="#4F46E5"
          borderStrokeWidth={2}
          anchorStroke="#4F46E5"
          anchorFill="#FFFFFF"
          anchorSize={10}
          anchorCornerRadius={5}
        />
      )}
    </>
  )
}
