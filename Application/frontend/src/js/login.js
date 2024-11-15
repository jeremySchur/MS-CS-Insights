const LOGIN_API_URL = `${import.meta.env.VITE_BACKEND_API_URL}/api/login`;

async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(LOGIN_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            window.location.href = '/index.html';
        } else {
            document.getElementById('error-message').innerText = 'Incorrect username or password';
        }
    } catch (error) {
        document.getElementById('error-message').innerText = 'An error occurred. Please try again.';
    }
}

document.getElementById('login-form').addEventListener('submit', handleLogin);