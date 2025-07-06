// Display user info
function displayUserInfo() {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user) {
    document.getElementById('userInfo').textContent = `Welcome, ${user.name}`;
    document.getElementById('logoutBtn').style.display = 'block';
  }
}

// Network status indicator
function setupNetworkStatus() {
  const statusElement = document.getElementById('networkStatus');
  
  function updateStatus() {
    if (navigator.onLine) {
      statusElement.textContent = 'Online';
      statusElement.style.backgroundColor = '#4CAF50';
      
      // Show connection restored message
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.textContent = 'Connection restored';
      document.body.appendChild(toast);
      setTimeout(() => toast.remove(), 3000);
    } else {
      statusElement.textContent = 'Offline';
      statusElement.style.backgroundColor = '#f44336';
      
      // Show offline message
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.textContent = 'You are offline';
      document.body.appendChild(toast);
    }
  }
  
  window.addEventListener('online', updateStatus);
  window.addEventListener('offline', updateStatus);
  updateStatus();
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  displayUserInfo();
  setupNetworkStatus();
  
  document.getElementById('logoutBtn').addEventListener('click', () => {
    logout();
  });
});
