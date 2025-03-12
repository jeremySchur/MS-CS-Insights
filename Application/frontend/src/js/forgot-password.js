const REQUEST_RESET_API_URL = `${import.meta.env.VITE_BACKEND_API_URL}/api/request-password-reset`;

async function handleForgotPassword(event) {
    event.preventDefault();
    const email = document.getElementById('email').value;
    try {
        const response = await fetch(REQUEST_RESET_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const result = await response.json();
        alert(result.message);
    } catch (error) {
        alert('An error occurred. Please try again.');
    }
}

document.getElementById('forgot-password-form').addEventListener('submit', handleForgotPassword);
document.getElementById('back-to-login').addEventListener('click', () => {
    window.location.href = 'login.html';
});
