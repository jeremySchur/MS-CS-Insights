document.getElementById('forgot-password-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const email = document.getElementById('email').value;

    alert(`If an account exists for ${email}, a password reset link will be sent.`);

    // Redirect back to login after a short delay
    setTimeout(() => {
        window.location.href = 'login.html';
    }, 2000);
});

document.getElementById('back-to-login').addEventListener('click', function () {
    window.location.href = 'login.html';
});
