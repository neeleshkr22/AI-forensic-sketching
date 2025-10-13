import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileImage, X } from 'lucide-react'
import toast from 'react-hot-toast'

export default function SketchUploader({ onComplete }) {
  const [uploadedFile, setUploadedFile] = useState(null)
  const [preview, setPreview] = useState(null)

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length === 0) return

    const file = acceptedFiles[0]

    // Validate file type
    if (!file.type.startsWith('image/')) {
      toast.error('Please upload an image file')
      return
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('File size must be less than 10MB')
      return
    }

    setUploadedFile(file)

    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      setPreview(e.target.result)
    }
    reader.readAsDataURL(file)

    toast.success('File uploaded successfully')
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif'],
    },
    multiple: false,
  })

  const handleRemove = () => {
    setUploadedFile(null)
    setPreview(null)
  }

  const handleSubmit = () => {
    if (!uploadedFile) {
      toast.error('Please upload a sketch first')
      return
    }

    onComplete({ file: uploadedFile })
  }

  return (
    <div className="space-y-6">
      {!uploadedFile ? (
        /* Drop Zone */
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400'
          }`}
        >
          <input {...getInputProps()} />
          <div className="flex flex-col items-center space-y-4">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center">
              <Upload className="w-8 h-8 text-primary-600" />
            </div>
            <div>
              <p className="text-lg font-semibold text-gray-800">
                {isDragActive ? 'Drop the file here' : 'Drag & drop a sketch image'}
              </p>
              <p className="text-gray-600 mt-2">
                or click to browse files
              </p>
            </div>
            <p className="text-sm text-gray-500">
              Supported formats: PNG, JPG, JPEG, GIF (max 10MB)
            </p>
          </div>
        </div>
      ) : (
        /* Preview */
        <div className="space-y-4">
          <div className="border-2 border-gray-200 rounded-lg p-4">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <FileImage className="w-6 h-6 text-primary-600" />
                <div>
                  <h4 className="font-semibold text-gray-800">Uploaded Sketch</h4>
                  <p className="text-sm text-gray-600">{uploadedFile.name}</p>
                </div>
              </div>
              <button
                onClick={handleRemove}
                className="p-2 text-gray-400 hover:text-red-600 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="bg-gray-50 rounded-lg p-4 flex items-center justify-center">
              <img
                src={preview}
                alt="Uploaded sketch"
                className="max-w-full max-h-96 rounded-lg shadow-md"
              />
            </div>

            <div className="mt-4 text-sm text-gray-600">
              <p>
                <strong>Size:</strong> {(uploadedFile.size / 1024).toFixed(2)} KB
              </p>
              <p>
                <strong>Type:</strong> {uploadedFile.type}
              </p>
            </div>
          </div>

          <button
            onClick={handleSubmit}
            className="btn-primary w-full"
          >
            Use This Sketch
          </button>
        </div>
      )}

      {/* Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-semibold text-blue-900 mb-2">Tips for best results:</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Use clear, high-contrast sketches</li>
          <li>• Face should be front-facing and well-centered</li>
          <li>• Avoid blurry or low-quality images</li>
          <li>• Black and white sketches work best</li>
        </ul>
      </div>
    </div>
  )
}
