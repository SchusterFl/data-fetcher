<template>
  <div class="dashboard-container">
    <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
      <!-- Summary cards -->
      <div class="bg-white rounded-lg shadow p-4">
        <h3 class="text-lg font-medium mb-2">Total Data Sources</h3>
        <p class="text-3xl font-bold">{{ totalDataSources }}</p>
      </div>
      
      <div class="bg-white rounded-lg shadow p-4">
        <h3 class="text-lg font-medium mb-2">Active Fetches</h3>
        <p class="text-3xl font-bold">{{ activeFetches }}</p>
      </div>
      
      <div class="bg-white rounded-lg shadow p-4">
        <h3 class="text-lg font-medium mb-2">Last Fetch</h3>
        <p class="text-xl">{{ lastFetchTime }}</p>
      </div>
    </div>
    
    <div class="mb-8">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Recent Data Sources</h2>
        <router-link to="/datasources" class="text-blue-600 hover:text-blue-800">
          View All
        </router-link>
      </div>
      
      <div v-if="recentDataSources.length" class="bg-white rounded-lg shadow">
        <DataSourceList :datasources="recentDataSources" :compact="true" />
      </div>
      <p v-else class="text-gray-500">No data sources available.</p>
    </div>
    
    <div>
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Recent Activity</h2>
      </div>
      
      <div v-if="recentActivity.length" class="bg-white rounded-lg shadow p-4">
        <ul class="divide-y">
          <li v-for="activity in recentActivity" :key="activity.id" class="py-3">
            <div class="flex items-center">
              <span class="mr-3">
                <span v-if="activity.type === 'success'" class="text-green-500">✓</span>
                <span v-else-if="activity.type === 'error'" class="text-red-500">✗</span>
                <span v-else class="text-yellow-500">⟳</span>
              </span>
              <div>
                <p class="font-medium">{{ activity.message }}</p>
                <p class="text-sm text-gray-500">{{ activity.timestamp }}</p>
              </div>
            </div>
          </li>
        </ul>
      </div>
      <p v-else class="text-gray-500">No recent activity.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useDataSourceStore } from '../stores/datasourceStore';
import DataSourceList from '../components/datasource/DataSourceList.vue';

const router = useRouter();
const dataSourceStore = useDataSourceStore();

// Dashboard data
const totalDataSources = ref(0);
const activeFetches = ref(0);
const lastFetchTime = ref('Never');
const recentDataSources = ref([]);
const recentActivity = ref([]);

onMounted(async () => {
  try {
    // Fetch dashboard data
    await dataSourceStore.fetchDataSources();
    
    // Update dashboard stats
    totalDataSources.value = dataSourceStore.dataSources.length;
    
    // Get only the 5 most recent data sources
    recentDataSources.value = dataSourceStore.dataSources
      .slice()
      .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
      .slice(0, 5);
    
    // Fetch activity logs (this would be a separate API call in a real app)
    // Mocking data for now
    recentActivity.value = [
      { 
        id: 1, 
        type: 'success', 
        message: 'Successfully fetched data from API endpoint', 
        timestamp: '2 hours ago',
        datasourceId: recentDataSources.value[0]?.id 
      },
      { 
        id: 2, 
        type: 'error', 
        message: 'Failed to connect to database', 
        timestamp: '5 hours ago',
        datasourceId: recentDataSources.value[1]?.id
      },
      { 
        id: 3, 
        type: 'pending', 
        message: 'Scheduled fetch in progress', 
        timestamp: '6 hours ago',
        datasourceId: recentDataSources.value[0]?.id
      }
    ];
    
    // Set other stats
    activeFetches.value = recentActivity.value.filter(a => a.type === 'pending').length;
    
    const successActivity = recentActivity.value.find(a => a.type === 'success');
    if (successActivity) {
      lastFetchTime.value = successActivity.timestamp;
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  }
});
</script>