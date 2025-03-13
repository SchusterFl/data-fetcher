import { defineStore } from 'pinia'
import { useApi } from '../composables/useApi'

export const useDataSourceStore = defineStore('datasource', {
  state: () => ({
    datasources: [],
    loading: false,
    error: null,
    currentDatasource: null
  }),
  
  getters: {
    getDatasourceById: (state) => (id) => {
      return state.datasources.find(ds => ds.id === id)
    }
  },
  
  actions: {
    async fetchDatasources() {
      const { datasourceApi } = useApi()
      this.loading = true
      this.error = null
      
      try {
        this.datasources = await datasourceApi.getAll()
      } catch (error) {
        this.error = error.message
        console.error('Failed to fetch datasources:', error)
      } finally {
        this.loading = false
      }
    },
    
    async fetchDatasourceById(id) {
      const { datasourceApi } = useApi()
      this.loading = true
      this.error = null
      
      try {
        this.currentDatasource = await datasourceApi.getById(id)
        return this.currentDatasource
      } catch (error) {
        this.error = error.message
        console.error(`Failed to fetch datasource with ID ${id}:`, error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async createDatasource(datasource) {
      const { datasourceApi } = useApi()
      this.loading = true
      this.error = null
      
      try {
        const newDatasource = await datasourceApi.create(datasource)
        this.datasources.push(newDatasource)
        return newDatasource
      } catch (error) {
        this.error = error.message
        console.error('Failed to create datasource:', error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async updateDatasource(id, datasource) {
      const { datasourceApi } = useApi()
      this.loading = true
      this.error = null
      
      try {
        const updatedDatasource = await datasourceApi.update(id, datasource)
        const index = this.datasources.findIndex(ds => ds.id === id)
        
        if (index !== -1) {
          this.datasources[index] = updatedDatasource
        }
        
        return updatedDatasource
      } catch (error) {
        this.error = error.message
        console.error(`Failed to update datasource with ID ${id}:`, error)
        return null
      } finally {
        this.loading = false
      }
    },
    
    async deleteDatasource(id) {
      const { datasourceApi } = useApi()
      this.loading = true
      this.error = null
      
      try {
        await datasourceApi.delete(id)
        this.datasources = this.datasources.filter(ds => ds.id !== id)
        return true
      } catch (error) {
        this.error = error.message
        console.error(`Failed to delete datasource with ID ${id}:`, error)
        return false
      } finally {
        this.loading = false
      }
    }
  }
})