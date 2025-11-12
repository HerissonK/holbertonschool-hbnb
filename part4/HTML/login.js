document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            if (!email || !password) {
                errorMessage.textContent = "Please enter both email and password.";
                return;
            }

            try {
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    // Stocke le token JWT dans un cookie
                    document.cookie = `token=${data.access_token}; path=/; max-age=${60*60*24}`; // 1 jour
                    // Redirection vers la page principale
                    window.location.href = 'index.html';
                } else {
                    const errorData = await response.json();
                    errorMessage.textContent = errorData.message || 'Login failed';
                }
            } catch (error) {
                console.error('Error logging in:', error);
                errorMessage.textContent = 'An error occurred. Please try again.';
            }
        });
    }
});
