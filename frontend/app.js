// Lumen Frontend App
const API_BASE = 'http://127.0.0.1:8000';
let token = localStorage.getItem('lumen_token');

// DOM Elements
const authSection = document.getElementById('auth-section');
const dashboardSection = document.getElementById('dashboard-section');
const signupForm = document.getElementById('signup-form');
const signupMessage = document.getElementById('signup-message');
const logoutBtn = document.getElementById('logout-btn');
const tutoringForm = document.getElementById('tutoring-form');
const assignmentForm = document.getElementById('assignment-form');
const getProgressBtn = document.getElementById('get-progress-btn');
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    if (token) {
        showDashboard();
    } else {
        showAuthForm();
    }
    setupEventListeners();
});

function setupEventListeners() {
    signupForm.addEventListener('submit', handleSignup);
    tutoringForm.addEventListener('submit', handleTutoring);
    assignmentForm.addEventListener('submit', handleAssignment);
    getProgressBtn.addEventListener('click', handleProgressRequest);
    logoutBtn.addEventListener('click', handleLogout);

    // Tab switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const tabName = e.target.dataset.tab;
            switchTab(tabName);
        });
    });
}

function showAuthForm() {
    authSection.classList.add('active');
    dashboardSection.classList.remove('active');
}

function showDashboard() {
    authSection.classList.remove('active');
    dashboardSection.classList.add('active');
    document.getElementById('student-name').textContent = localStorage.getItem('lumen_email') || 'Student';
}

async function handleSignup(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const age = parseInt(document.getElementById('age').value);
    const gradeLevel = document.getElementById('grade').value;

    // Age verification
    if (age < 13) {
        showMessage('You must be at least 13 years old to use Lumen.', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email,
                age,
                grade_level: gradeLevel
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Store token and email
            localStorage.setItem('lumen_token', data.access_token);
            localStorage.setItem('lumen_email', email);
            
            showMessage('Signup successful! Welcome to Lumen!', 'success');
            setTimeout(() => {
                signupForm.reset();
                showDashboard();
            }, 1500);
        } else {
            showMessage(data.detail || 'Signup failed. Please try again.', 'error');
        }
    } catch (error) {
        console.error('Signup error:', error);
        showMessage('Network error. Please try again.', 'error');
    }
}

async function handleTutoring(e) {
    e.preventDefault();

    const topic = document.getElementById('topic').value;
    const understanding = document.getElementById('understanding').value;
    const responseDiv = document.getElementById('tutoring-response');

    responseDiv.innerHTML = '<p><em>Thinking...</em></p>';

    try {
        const response = await fetch(`${API_BASE}/tutoring/explain`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                topic,
                current_understanding: understanding
            })
        });

        const data = await response.json();

        if (response.ok) {
            responseDiv.innerHTML = `
                <p><strong>Explanation:</strong></p>
                <p>${data.explanation}</p>
                <p><strong>Next Question:</strong></p>
                <p>${data.next_question}</p>
            `;
            tutoringForm.reset();
        } else {
            responseDiv.innerHTML = `<p class="error">Error: ${data.detail || 'Failed to get response'}</p>`;
        }
    } catch (error) {
        console.error('Tutoring error:', error);
        responseDiv.innerHTML = '<p class="error">Network error. Please try again.</p>';
    }
}

async function handleAssignment(e) {
    e.preventDefault();

    const assignment = document.getElementById('assignment-name').value;
    const submission = document.getElementById('submission').value;
    const responseDiv = document.getElementById('assignment-response');

    responseDiv.innerHTML = '<p><em>Reviewing your work...</em></p>';

    try {
        const response = await fetch(`${API_BASE}/assignments/submit`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                assignment,
                submission
            })
        });

        const data = await response.json();

        if (response.ok) {
            responseDiv.innerHTML = `
                <p><strong>Academic Integrity Check:</strong></p>
                <p style="color: ${data.academic_integrity_check === 'PASSED' ? 'green' : 'red'};">
                    ${data.academic_integrity_check === 'PASSED' ? '✓ Safe to proceed' : '⚠ Review needed'}
                </p>
                <p><strong>Feedback:</strong></p>
                <p>${data.feedback}</p>
            `;
            assignmentForm.reset();
        } else {
            responseDiv.innerHTML = `<p class="error">Error: ${data.detail || 'Failed to process submission'}</p>`;
        }
    } catch (error) {
        console.error('Assignment error:', error);
        responseDiv.innerHTML = '<p class="error">Network error. Please try again.</p>';
    }
}

async function handleProgressRequest() {
    const progressDiv = document.getElementById('progress-report');
    progressDiv.innerHTML = '<p><em>Generating your progress report...</em></p>';

    try {
        const response = await fetch(`${API_BASE}/progress`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            let subjectsHTML = '';
            for (const [subject, level] of Object.entries(data.subjects)) {
                subjectsHTML += `<li><strong>${subject.charAt(0).toUpperCase() + subject.slice(1)}:</strong> ${level}</li>`;
            }

            progressDiv.innerHTML = `
                <p><strong>Overall Proficiency:</strong> ${data.overall_proficiency}</p>
                <p><strong>By Subject:</strong></p>
                <ul>${subjectsHTML}</ul>
                <p><strong>Recommendation:</strong></p>
                <p>${data.recommendations}</p>
                <p><em>Last updated: ${new Date(data.last_updated).toLocaleDateString()}</em></p>
            `;
        } else {
            progressDiv.innerHTML = `<p class="error">Error: ${data.detail || 'Failed to load progress'}</p>`;
        }
    } catch (error) {
        console.error('Progress error:', error);
        progressDiv.innerHTML = '<p class="error">Network error. Please try again.</p>';
    }
}

function switchTab(tabName) {
    // Hide all tabs
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    // Deactivate all buttons
    tabBtns.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Activate selected button
    const selectedBtn = document.querySelector(`[data-tab="${tabName}"]`);
    if (selectedBtn) {
        selectedBtn.classList.add('active');
    }
}

function handleLogout() {
    localStorage.removeItem('lumen_token');
    localStorage.removeItem('lumen_email');
    token = null;
    showAuthForm();
    signupForm.reset();
    signupMessage.textContent = '';
}

function showMessage(message, type) {
    signupMessage.textContent = message;
    signupMessage.className = type;
    if (type === 'success') {
        setTimeout(() => {
            signupMessage.textContent = '';
        }, 3000);
    }
}

// Simple health check
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (!response.ok) {
            console.warn('API health check failed');
        }
    } catch (error) {
        console.error('Cannot connect to API. Ensure the server is running on localhost:8000');
    }
}

checkHealth();
