import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Sketch API
export const sketchAPI = {
  generateFromPrompt: async (prompt, userId = null) => {
    const response = await api.post('/api/sketch/generate', { prompt, user_id: userId })
    return response.data
  },

  composeFromComponents: async (components, userId = null) => {
    const response = await api.post('/api/sketch/compose', { components, user_id: userId })
    return response.data
  },

  uploadSketch: async (file, userId = null) => {
    const formData = new FormData()
    formData.append('file', file)
    if (userId) formData.append('user_id', userId)

    const response = await api.post('/api/sketch/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  searchWithSketch: async (fileOrSketchData, topK = 10, threshold = 0.5) => {
    // Check if we have a File object or sketch data with URL/ID
    if (fileOrSketchData instanceof File) {
      // Use multipart form data for file upload
      const formData = new FormData()
      formData.append('file', fileOrSketchData)
      formData.append('top_k', topK)
      formData.append('threshold', threshold)

      const response = await api.post('/api/sketch/search', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      return response.data
    } else {
      // Use JSON for sketch URL/ID (from generated sketches)
      const payload = {
        top_k: topK,
        threshold: threshold
      }
      
      // Check for sketch_id first, then sketch_url
      if (fileOrSketchData.sketch_id) {
        payload.sketch_id = fileOrSketchData.sketch_id
      } else if (fileOrSketchData.sketch_url) {
        payload.sketch_url = fileOrSketchData.sketch_url
      } else if (typeof fileOrSketchData === 'string') {
        payload.sketch_url = fileOrSketchData
      } else {
        // Fallback - try to extract any URL-like property
        payload.sketch_url = fileOrSketchData.url || fileOrSketchData.path || fileOrSketchData
      }
      
      // Pass prompt/description for intelligent matching
      if (fileOrSketchData.prompt) {
        payload.prompt = fileOrSketchData.prompt
      } else if (fileOrSketchData.description) {
        payload.prompt = fileOrSketchData.description
      }
      
      const response = await api.post('/api/sketch/search', payload)
      return response.data
    }
  },

  getRecentSketches: async (userId = null, limit = 20) => {
    const params = { limit }
    if (userId) params.user_id = userId

    const response = await api.get('/api/sketch/recent', { params })
    return response.data
  },

  getSketchImage: (sketchId) => {
    return `${API_BASE_URL}/api/sketch/image/${sketchId}`
  },

  getServiceStatus: async () => {
    const response = await api.get('/api/sketch/status')
    return response.data
  },
}

// Records API
export const recordsAPI = {
  getAll: async (skip = 0, limit = 100, filters = {}) => {
    const params = { skip, limit, ...filters }
    const response = await api.get('/api/records', { params })
    return response.data
  },

  getById: async (recordId) => {
    const response = await api.get(`/api/records/${recordId}`)
    return response.data
  },

  create: async (recordData, photoFile = null) => {
    const formData = new FormData()
    
    Object.keys(recordData).forEach(key => {
      if (recordData[key] !== null && recordData[key] !== undefined) {
        formData.append(key, recordData[key])
      }
    })

    if (photoFile) {
      formData.append('photo', photoFile)
    }

    const response = await api.post('/api/records', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  update: async (recordId, updateData, photoFile = null) => {
    const formData = new FormData()
    
    Object.keys(updateData).forEach(key => {
      if (updateData[key] !== null && updateData[key] !== undefined) {
        formData.append(key, updateData[key])
      }
    })

    if (photoFile) {
      formData.append('photo', photoFile)
    }

    const response = await api.put(`/api/records/${recordId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  delete: async (recordId) => {
    const response = await api.delete(`/api/records/${recordId}`)
    return response.data
  },

  search: async (query) => {
    const response = await api.get('/api/records/search', { params: { q: query } })
    return response.data
  },

  getPhoto: (recordId) => {
    return `${API_BASE_URL}/api/records/photo/${recordId}`
  },

  getStats: async () => {
    const response = await api.get('/api/records/stats')
    return response.data
  },
}

// Features API
export const featuresAPI = {
  extractFeatures: async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/api/features/extract', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  detectFace: async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/api/features/detect-face', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  photoToSketch: async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/api/features/photo-to-sketch', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  enhanceImage: async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/api/features/enhance', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  getModelInfo: async () => {
    const response = await api.get('/api/features/model-info')
    return response.data
  },
}

export default api
