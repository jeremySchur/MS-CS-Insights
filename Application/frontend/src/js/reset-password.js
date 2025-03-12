const RESET_PASSWORD_API_URL = `${import.meta.env.VITE_BACKEND_API_URL}/api/reset-password`;

async function handleResetPassword(event) {
    event.preventDefault();
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    const newPassword = document.getElementById('new-password').value;
    try {
        const response = await fetch(RESET_PASSWORD_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token, newPassword })  // <-- Remove `newPassword: newPassword`
        });
        const result = await response.json();
        if (response.ok) {
            alert('Password reset successful!');
            window.location.href = 'login.html';
        } else {
            alert(result.message || "Something went wrong. Please try again.");
        }
    } catch (error) {
        alert('An error occurred. Please try again.');
    }
}

document.getElementById('reset-password-form').addEventListener('submit', handleResetPassword);
document.getElementById('back-to-login').addEventListener('click', () => {
    window.location.href = 'login.html';
});
