import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const apiService = {
  // Upload endpoints
  uploadStatement: async (file, issuer = null) => {
    const formData = new FormData()
    formData.append('file', file)
    if (issuer) {
      formData.append('issuer', issuer)
    }
    
    return api.post('/api/v1/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  uploadBatch: async (files, issuer = null) => {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })
    if (issuer) {
      formData.append('issuer', issuer)
    }
    
    return api.post('/api/v1/upload-batch', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // Statement endpoints
  getStatements: async (params = {}) => {
    return api.get('/api/v1/statements', { params })
  },

  getStatement: async (id) => {
    return api.get(`/api/v1/statements/${id}`)
  },

  updateStatement: async (id, data) => {
    return api.put(`/api/v1/statements/${id}`, data)
  },

  deleteStatement: async (id) => {
    return api.delete(`/api/v1/statements/${id}`)
  },

  reprocessStatement: async (id) => {
    return api.get(`/api/v1/statements/${id}/reprocess`)
  },

  // Stats endpoints
  getStats: async () => {
    return api.get('/api/v1/statements/stats/summary')
  },

  // Health check
  getHealth: async () => {
    return api.get('/health')
  },
}

export { api }
