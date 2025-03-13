<template>
  <div class="datasource-container">
    <div class="mb-8">
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold">Data Sources</h1>
        <button 
          @click="openCreateModal" 
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
        >
          Add New Data Source
        </button>
      </div>
      
      <div class="bg-white rounded-lg shadow p-4 mb-4">
        <div class="flex flex-col md:flex-row gap-4">
          <div class="flex-1">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Search data sources..." 
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div class="flex-initial">
            <select 
              v-model="statusFilter" 
              class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Statuses</option>
              <option value="active">Active</option>
              <option value="paused">Paused</option>
              <option value="error">Error</option>
            </select>
          </div>
        </div>
      </div>
    </div>
    
    <div class="data-source-list">
      <div v-if="loading" class="text-center py-8">
        <p>Loading data sources...</p>
      </div>
      
      <div v-else-if="filteredDataSources.length === 0" class="text-center py-8 bg-white rounded-lg shadow">
        <p class="text-gray-500">No data sources found.</p>
        <button 
          @click="openCreateModal" 
          class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
        >
          Create your first data source
        </button>
      </div>
      
      <DataSourceList 
        v-else 
        :datasources="filteredDataSources" 
        :compact="false"
        @edit="editDataSource"
        @delete="confirmDeleteDataSource"
        @toggle-status="toggleDataSourceStatus"
      />
    </div>
    
    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-xl">
        <h2 class="text-xl font-bold mb-4">
          {{ isEditing ? 'Edit Data Source' : 'Create New Data Source' }}
        </h2>
        
        <DataSourceForm 
          :initialData="currentDataSource" 
          @submit="saveDataSource" 
          @cancel="closeModal"
        />
      </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-bold mb-4">Confirm Delete</h2>
        <p class="mb-6">Are you sure you want to delete this data source? This action cannot be undone.</p>
        
        <div class="flex justify-end gap-3">
          <button 
            @click="showDeleteModal = false" 
            class="px-4 py-2 border rounded hover:bg-gray-100 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="deleteDataSource" 
            class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useDataSourceStore } from '../stores/datasourceStore';
import DataSourceList from '../components/datasource/DataSourceList.vue';
import DataSourceForm from '../components/datasource/DataSourceForm.vue';

const dataSourceStore = useDataSourceStore();

// State
const loading = ref(true);
const searchQuery = ref('');
const statusFilter = ref('all');
const showModal = ref(false);
const showDeleteModal = ref(false);
const isEditing = ref(false);
const currentDataSource = ref({
  id: null,
  name: '',
  type: 'api',
  endpoint: '',
  authType: 'none',
  credentials: {},
  schedule: '0 0 * * *', // Default: daily at midnight
  status: 'active'
});
const dataSourceToDelete = ref(null);

// Computed properties
const filteredDataSources = computed(() => {
  let filtered = dataSourceStore.dataSources;
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(ds => 
      ds.name.toLowerCase().includes(query) || 
      ds.endpoint.toLowerCase().includes(query)
    );
  }
  
  // Apply status filter
  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(ds => ds.status === statusFilter.value);
  }
  
  return filtered;
});

// Methods
const openCreateModal = () => {
  isEditing.value = false;
  currentDataSource.value = {
    id: null,
    name: '',
    type: 'api',
    endpoint: '',
    authType: 'none',
    credentials: {},
    schedule: '0 0 * * *',
    status: 'active'
  };
  showModal.value = true;
};

const editDataSource = (dataSource) => {
  isEditing.value = true;
  currentDataSource.value = { ...dataSource };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const saveDataSource = async (formData) => {
  try {
    if (isEditing.value) {
      await dataSourceStore.updateDataSource({ ...formData, id: currentDataSource.value.id });
    } else {
      await dataSourceStore.createDataSource(formData);
    }
    closeModal();
  } catch (error) {
    console.error('Error saving data source:', error);
  }
};

const confirmDeleteDataSource = (dataSource) => {
  dataSourceToDelete.value = dataSource;
  showDeleteModal.value = true;
};

const deleteDataSource = async () => {
  try {
    await dataSourceStore.deleteDataSource(dataSourceToDelete.value.id);
    showDeleteModal.value = false;
    dataSourceToDelete.value = null;
  } catch (error) {
    console.error('Error deleting data source:', error);
  }
};

const toggleDataSourceStatus = async (dataSource) => {
  try {
    const newStatus = dataSource.status === 'active' ? 'paused' : 'active';
    await dataSourceStore.updateDataSource({ 
      ...dataSource, 
      status: newStatus 
    });
  } catch (error) {
    console.error('Error updating data source status:', error);
  }
};

// Lifecycle hooks
onMounted(async () => {
  try {
    await dataSourceStore.fetchDataSources();
  } catch (error) {
    console.error('Error fetching data sources:', error);
  } finally {
    loading.value = false;
  }
});

// Watch for store changes
watch(() => dataSourceStore.dataSources, (newSources) => {
  // Handle store updates if needed
}, { deep: true });
</script>