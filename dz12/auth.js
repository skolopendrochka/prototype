document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  
  // Validate email
  if (!validateEmail(email)) {
    document.getElementById('emailError').textContent = 'Invalid email format';
    return;
  } else {
    document.getElementById('emailError').textContent = '';
  }
  
  // Validate password
  if (password.length < 6) {
    document.getElementById('passwordError').textContent = 'Password must be at least 6 characters';
    return;
  } else {
    document.getElementById('passwordError').textContent = '';
  }
  
  try {
    // Simulate API call
    const response = await fakeAuthAPI(email, password);
    
    // Save token to localStorage
    localStorage.setItem('authToken', response.token);
    localStorage.setItem('user', JSON.stringify(response.user));
    
    // Redirect to main app
    window.location.href = 'index.html';
  } catch (error) {
    document.getElementById('loginError').textContent = error.message;
  }
});

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

// Fake auth API function
async function fakeAuthAPI(email, password) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (email === 'user@example.com' && password === 'password123') {
        resolve({
          token: 'fake-jwt-token-123456',
          user: { name: 'John Doe', email: 'user@example.com' }
        });
      } else {
        reject(new Error('Invalid credentials'));
      }
    }, 1000);
  });
}

// Check auth status on app load
function checkAuth() {
  const token = localStorage.getItem('authToken');
  if (!token && !window.location.pathname.endsWith('login.html')) {
    window.location.href = 'login.html';
  }
}

// Logout function
function logout() {
  localStorage.removeItem('authToken');
  localStorage.removeItem('user');
  window.location.href = 'login.html';
}

// Initialize auth check
checkAuth();
