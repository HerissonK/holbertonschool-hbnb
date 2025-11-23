// Attendre que tout le HTML soit chargé avant d'exécuter le script
document.addEventListener('DOMContentLoaded', () => {

    // Récupération du formulaire de login et du conteneur d'erreur
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    // Vérifie si le formulaire existe sur la page (permet d'éviter des erreurs)
    if (loginForm) {

        // Écoute la soumission du formulaire
        loginForm.addEventListener('submit', async (event) => {

            // Empêche le rechargement de la page
            event.preventDefault();

            // Récupère les valeurs du formulaire
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            // Vérifie que les champs ne sont pas vides
            if (!email || !password) {
                errorMessage.textContent = "Please enter both email and password.";
                return;
            }

            try {
                // Envoie la requête de connexion à l'API
                const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password }) // Envoi des identifiants
                });

                // Si la connexion réussit
                if (response.ok) {
                    const data = await response.json();

                    // Stocke le token JWT dans un cookie valable 24h
                    document.cookie = `token=${data.access_token}; path=/; max-age=${60 * 60 * 24}`;

                    // Redirection vers la page d'accueil
                    window.location.href = 'index.html';

                } else {
                    // Si l'API renvoie une erreur (mauvais email/mot de passe)
                    const errorData = await response.json();
                    errorMessage.textContent = errorData.message || 'Login failed';
                }

            } catch (error) {
                // Si une erreur réseau survient
                console.error('Error logging in:', error);
                errorMessage.textContent = 'An error occurred. Please try again.';
            }
        });
    }
});
