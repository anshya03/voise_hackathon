// Authentication JavaScript with SQLite backend
let currentUser = null;

// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');
const showSignupLink = document.getElementById('showSignup');
const showLoginLink = document.getElementById('showLogin');
const loadingOverlay = document.getElementById('loadingOverlay');

// Initialize authentication page
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    checkAuthStatus();
    
    // Add event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Form switching
    showSignupLink.addEventListener('click', function(e) {
        e.preventDefault();
        showSignupForm();
    });
    
    showLoginLink.addEventListener('click', function(e) {
        e.preventDefault();
        showLoginForm();
    });
    
    // Form submissions
    loginForm.addEventListener('submit', handleLogin);
    signupForm.addEventListener('submit', handleSignup);
}

function showSignupForm() {
    loginForm.classList.add('hidden');
    signupForm.classList.remove('hidden');
    clearMessages();
}

function showLoginForm() {
    signupForm.classList.add('hidden');
    loginForm.classList.remove('hidden');
    clearMessages();
}

async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    
    if (!email || !password) {
        showMessage('Please fill in all fields', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Login failed');
        }
        
        // Store user session
        const userData = {
            ...result.user,
            session_id: result.session_id
        };
        
        localStorage.setItem('currentUser', JSON.stringify(userData));
        currentUser = userData;
        
        showMessage('Login successful! Redirecting...', 'success');
        
        // Redirect to main app after short delay
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1500);
        
    } catch (error) {
        console.error('Login error:', error);
        showMessage(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function handleSignup(e) {
    e.preventDefault();
    
    const name = document.getElementById('signupName').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const agreeTerms = document.getElementById('agreeTerms').checked;
    
    // Validation
    if (!name || !email || !password || !confirmPassword) {
        showMessage('Please fill in all fields', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showMessage('Passwords do not match', 'error');
        return;
    }
    
    if (password.length < 6) {
        showMessage('Password must be at least 6 characters long', 'error');
        return;
    }
    
    if (!agreeTerms) {
        showMessage('Please agree to the Terms of Service', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Signup failed');
        }
        
        showMessage('Account created successfully! Please login with your credentials.', 'success');
        
        // Clear the form
        document.getElementById('signupForm').reset();
        
        // Redirect to login form after short delay
        setTimeout(() => {
            showLoginForm();
        }, 2000);
        
    } catch (error) {
        console.error('Signup error:', error);
        showMessage(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

async function checkAuthStatus() {
    const savedUser = localStorage.getItem('currentUser');
    if (!savedUser) {
        return; // No saved user
    }
    
    try {
        const userData = JSON.parse(savedUser);
        
        // Verify session with backend
        const response = await fetch(`${API_BASE_URL}/auth/verify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: userData.session_id
            })
        });
        
        if (response.ok) {
            // Session is valid, redirect to main app
            currentUser = userData;
            window.location.href = 'index.html';
        } else {
            // Session invalid, remove from localStorage
            localStorage.removeItem('currentUser');
        }
    } catch (error) {
        console.error('Session verification error:', error);
        localStorage.removeItem('currentUser');
    }
}

function showLoading(show) {
    if (show) {
        loadingOverlay.classList.add('show');
    } else {
        loadingOverlay.classList.remove('show');
    }
}

function showMessage(text, type) {
    // Remove any existing messages
    clearMessages();
    
    // Create message element
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;
    
    // Insert message at the beginning of the active form
    const activeForm = document.querySelector('.auth-form:not(.hidden)');
    const formTitle = activeForm.querySelector('h2');
    formTitle.insertAdjacentElement('afterend', message);
    
    // Auto-remove success messages
    if (type === 'success') {
        setTimeout(() => {
            if (message.parentNode) {
                message.remove();
            }
        }, 3000);
    }
}

function clearMessages() {
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => msg.remove());
}

// Export functions for potential use in other files
window.authUtils = {
    getCurrentUser: () => currentUser,
    logout: async () => {
        if (currentUser && currentUser.session_id) {
            try {
                await fetch(`${API_BASE_URL}/auth/logout`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        session_id: currentUser.session_id
                    })
                });
            } catch (error) {
                console.error('Logout error:', error);
            }
        }
        
        // Clear all user and medicine data
        localStorage.removeItem('currentUser');
        localStorage.removeItem('lastSessionId');
        localStorage.removeItem('doctorA');
        localStorage.removeItem('doctorB');
        localStorage.removeItem('userAllergies');
        currentUser = null;
        window.location.href = 'login.html';
    },
    isLoggedIn: () => !!currentUser
};