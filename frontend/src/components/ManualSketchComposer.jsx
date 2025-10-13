import { useState, useRef, useEffect } from 'react'
import { Stage, Layer, Image as KonvaImage, Transformer } from 'react-konva'
import { Download, Trash2, RotateCw, ZoomIn, ZoomOut } from 'lucide-react'
import toast from 'react-hot-toast'

// Facial components with actual images
const facialComponents = {
  eyes: [
    { id: 'eyes1', name: 'Round Eyes', url: '/assets/face-parts/eye1.png' },
    { id: 'eyes2', name: 'Almond Eyes', url: '/assets/face-parts/eye2.png' },
    { id: 'eyes3', name: 'Narrow Eyes', url: '/assets/face-parts/eye3.png' },
    { id: 'eyes4', name: 'Wide Eyes', url: '/assets/face-parts/eye4.png' },
  ],
  nose: [
    { id: 'nose1', name: 'Straight Nose', url: '/assets/face-parts/nose1.png' },
    { id: 'nose2', name: 'Button Nose', url: '/assets/face-parts/nose2.png' },
    { id: 'nose3', name: 'Hook Nose', url: '/assets/face-parts/nose3.png' },
    { id: 'nose4', name: 'Broad Nose', url: '/assets/face-parts/nose4.png' },
  ],
  mouth: [
    { id: 'mouth1', name: 'Thin Lips', url: '/assets/face-parts/mouth1.png' },
    { id: 'mouth2', name: 'Full Lips', url: '/assets/face-parts/mouth2.png' },
    { id: 'mouth3', name: 'Wide Mouth', url: '/assets/face-parts/mouth3.png' },
    { id: 'mouth4', name: 'Small Mouth', url: '/assets/face-parts/mouth4.png' },
  ],
  hair: [
    { id: 'hair1', name: 'Short Hair', url: '/assets/face-parts/hair1.png' },
    { id: 'hair2', name: 'Long Hair', url: '/assets/face-parts/hair2.png' },
    { id: 'hair3', name: 'Curly Hair', url: '/assets/face-parts/hair3.png' },
    { id: 'hair4', name: 'Bald', url: '/assets/face-parts/hair4.png' },
  ],
  face: [
    { id: 'face1', name: 'Oval Face', url: '/assets/face-parts/face1.png' },
    { id: 'face2', name: 'Round Face', url: '/assets/face-parts/face2.png' },
    { id: 'face3', name: 'Square Face', url: '/assets/face-parts/face3.png' },
    { id: 'face4', name: 'Long Face', url: '/assets/face-parts/face4.png' },
  ],
}

export default function ManualSketchComposer({ onComplete }) {
  const [selectedCategory, setSelectedCategory] = useState('face')
  const [placedComponents, setPlacedComponents] = useState([])
  const [selectedId, setSelectedId] = useState(null)
  const stageRef = useRef(null)

  const handleComponentClick = (component) => {
    // Add component to canvas
    const newComponent = {
      id: `${component.id}_${Date.now()}`,
      imageUrl: component.url,
      x: 200,
      y: 200,
      scale: 1,
      rotation: 0,
    }
    setPlacedComponents([...placedComponents, newComponent])
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
      toast.success('Component removed')
    }
  }

  const handleSave = () => {
    if (placedComponents.length === 0) {
      toast.error('Please add some components first')
      return
    }

    // Export canvas as image
    const stage = stageRef.current
    const dataURL = stage.toDataURL()

    // Convert to blob and create file
    fetch(dataURL)
      .then((res) => res.blob())
      .then((blob) => {
        const file = new File([blob], 'sketch.png', { type: 'image/png' })
        onComplete({ file, components: placedComponents })
      })
  }

  return (
    <div className="grid md:grid-cols-4 gap-6">
      {/* Component Library */}
      <div className="md:col-span-1 space-y-4">
        <h3 className="text-lg font-semibold text-gray-800">Components</h3>

        {/* Category Tabs */}
        <div className="space-y-2">
          {Object.keys(facialComponents).map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`w-full text-left px-4 py-2 rounded-lg capitalize transition-colors ${
                selectedCategory === category
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
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
              className="bg-white border-2 border-gray-200 rounded-lg p-3 cursor-pointer hover:border-primary-400 hover:shadow-md transition-all"
            >
              <div className="aspect-square bg-gray-50 rounded-md mb-2 flex items-center justify-center overflow-hidden">
                <img 
                  src={component.url} 
                  alt={component.name}
                  className="w-full h-full object-contain"
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'flex';
                  }}
                />
                <span className="text-gray-400 text-xs hidden">No Preview</span>
              </div>
              <p className="text-sm font-medium text-center">{component.name}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Canvas */}
      <div className="md:col-span-3">
        <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg p-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Canvas</h3>
            <div className="flex space-x-2">
              <button
                onClick={handleDelete}
                disabled={!selectedId}
                className="p-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 disabled:opacity-50 disabled:cursor-not-allowed"
                title="Delete selected"
              >
                <Trash2 className="w-5 h-5" />
              </button>
              <button
                onClick={handleSave}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 flex items-center space-x-2"
              >
                <Download className="w-5 h-5" />
                <span>Save Sketch</span>
              </button>
            </div>
          </div>

          {/* Konva Stage */}
          <div className="bg-gray-50 rounded-lg" style={{ width: '600px', height: '600px' }}>
            <Stage
              ref={stageRef}
              width={600}
              height={600}
              onClick={(e) => {
                // Deselect when clicking on empty area
                if (e.target === e.target.getStage()) {
                  setSelectedId(null)
                }
              }}
            >
              <Layer>
                {placedComponents.map((comp) => (
                  <ComponentImage
                    key={comp.id}
                    component={comp}
                    isSelected={comp.id === selectedId}
                    onSelect={() => setSelectedId(comp.id)}
                    onChange={(attrs) => handleTransform(comp.id, attrs)}
                  />
                ))}
              </Layer>
            </Stage>
          </div>

          <p className="text-sm text-gray-600 mt-4">
            Click components from the left panel to add them. Drag to move, use corner handles to resize and rotate.
          </p>
        </div>
      </div>
    </div>
  )
}

// Component for individual placed items
function ComponentImage({ component, isSelected, onSelect, onChange }) {
  const shapeRef = useRef()
  const trRef = useRef()
  const [image, setImage] = useState(null)

  // Load image
  useEffect(() => {
    const img = new window.Image()
    img.src = component.imageUrl
    img.onload = () => setImage(img)
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
        scaleX={component.scale}
        scaleY={component.scale}
        rotation={component.rotation}
        draggable
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

          onChange({
            x: node.x(),
            y: node.y(),
            scale: Math.max(scaleX, scaleY),
            rotation: node.rotation(),
          })
        }}
      />
      {isSelected && <Transformer ref={trRef} />}
    </>
  )
}
