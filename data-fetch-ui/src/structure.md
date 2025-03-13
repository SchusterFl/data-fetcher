frontend/
├── src/
│   ├── assets/              # Static assets
│   ├── components/          # Reusable components
│   │   ├── ui/              # UI components (shadcn)
│   │   └── datasource/      # Datasource specific components
│   │       ├── DataSourceForm.vue
│   │       ├── DataSourceList.vue
│   │       └── DataSourceListItem.vue
│   ├── composables/         # Reusable Vue composables
│   │   └── useApi.js        # API communication
│   ├── views/               # Page components
│   │   ├── DashboardView.vue
│   │   ├── DataSourceView.vue
│   │   └── NotFoundView.vue
│   ├── router/              # Vue Router configuration
│   │   └── index.js
│   ├── stores/              # Pinia stores
│   │   └── datasourceStore.js
│   ├── App.vue              # Root component
│   └── main.js              # Entry point
├── .gitignore
├── index.html
├── package.json
└── vite.config.js