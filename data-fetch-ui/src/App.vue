<template>
  <div class="app-container">
    <header>
      <h1>Data Fetch & Process</h1>
      <nav>
        <router-link to="/">Dashboard</router-link> |
        <router-link to="/datasources">Datenquellen</router-link>
      </nav>
    </header>
    
    <main>
      <router-view />
    </main>
    
    <footer>
      <p>Data Fetch & Process App</p>
    </footer>
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
}

header h1 {
  margin: 0 0 1rem;
}

nav {
  margin-bottom: 1rem;
}

nav a {
  color: white;
  text-decoration: none;
  margin-right: 1rem;
}

nav a.router-link-active {
  font-weight: bold;
  border-bottom: 2px solid white;
}

main {
  flex: 1;
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

footer {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
  text-align: center;
}
</style>