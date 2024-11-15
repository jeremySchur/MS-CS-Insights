console.log("login.js loaded");

const LOGIN_API_URL = `${import.meta.env.VITE_BACKEND_API_URL}/api/login`;

// Function to handle login form submission
async function handleLogin(event) {
    event.preventDefault(); // Prevent default form submission behavior

    // Get the values from the form fields
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        // Send a POST request to the login API
        console.log("Sending login request to:", LOGIN_API_URL);
        const response = await fetch(LOGIN_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password }) // Send username and password as JSON
        });

        console.log("Received response status:", response.status); // Log the status code

        if (response.ok) {
            // If login is successful, redirect to the main page
            console.log("Login successful, redirecting to home page.");
            window.location.href = '/index.html';
        } else {
            // If login fails, display an error message
            console.log("Login failed, incorrect username or password.");
            document.getElementById('error-message').innerText = 'Incorrect username or password';
        }
    } catch (error) {
        console.error('Error during login:', error);
        document.getElementById('error-message').innerText = 'An error occurred. Please try again.';
    }
}

// Attach the function to the form submission event
document.getElementById('login-form').addEventListener('submit', handleLogin);