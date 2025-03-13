const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export function useApi() {
  /**
   * General API request function
   */
  const apiRequest = async (endpoint, options = {}) => {
    const url = `${API_BASE_URL}${endpoint}`
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
    }
    
    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    }
    
    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `API error: ${response.status}`)
      }
      
      // For 204 No Content responses
      if (response.status === 204) {
        return null
      }
      
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }
  
  /**
   * DataSource specific API functions
   */
  const datasourceApi = {
    getAll: (skip = 0, limit = 100) => {
      return apiRequest(`/datasources/?skip=${skip}&limit=${limit}`)
    },
    
    getById: (id) => {
      return apiRequest(`/datasources/${id}`)
    },
    
    create: (datasource) => {
      return apiRequest('/datasources/', {
        method: 'POST',
        body: JSON.stringify(datasource),
      })
    },
    
    update: (id, datasource) => {
      return apiRequest(`/datasources/${id}`, {
        method: 'PUT',
        body: JSON.stringify(datasource),
      })
    },
    
    delete: (id) => {
      return apiRequest(`/datasources/${id}`, {
        method: 'DELETE',
      })
    }
  }
  
  return {
    datasourceApi
  }
}