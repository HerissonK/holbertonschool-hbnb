// === UTILITY ===
// Fonction utilitaire pour récupérer un cookie par son nom.
// Elle recherche dans document.cookie et renvoie la valeur correspondante si trouvée.
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// === CHECK AUTHENTICATION ===
// Vérifie que l'utilisateur possède un token valide.
// Si aucun token n'existe, l'utilisateur est redirigé vers la page de connexion
// car on impose la connexion pour ajouter une review.
function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        alert('You must be logged in to add a review.');
        window.location.href = 'login.html';
    }
    return token;
}

// === GET PLACE ID FROM URL ===
// Récupère l'ID du lieu depuis les paramètres de l'URL.
// Exemple : add_review.html?id=123 → renvoie "123".
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// === SUBMIT REVIEW ===
// Envoie une nouvelle review vers l’API.
// Pour cela, on envoie une requête POST avec le token JWT, le texte, la note et l'id du lieu.
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` // Permet de prouver que l'utilisateur est connecté
            },
            body: JSON.stringify({
                text: reviewText,
                rating: rating,
                place_id: placeId
            })
        });

        // Si la requête échoue, on tente de récupérer le message d’erreur précis fourni par l'API.
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to submit review');
        }

        // Succès → message + redirection vers la page du lieu
        alert('Review submitted successfully!');
        window.location.href = `place.html?id=${placeId}`;
    } catch (error) {
        alert('Error submitting review: ' + error.message);
    }
}

// === EVENT LISTENER ===
// Exécuté lorsque le DOM est chargé.
document.addEventListener('DOMContentLoaded', () => {

    // 1. Vérifie que l'utilisateur est connecté.
    const token = checkAuthentication();

    // 2. Récupère l’ID du lieu depuis l’URL.
    const placeId = getPlaceIdFromURL();

    // 3. Cache le bouton login si utilisateur connecté.
    const loginLink = document.getElementById('login-link');
    if (token && loginLink) {
        loginLink.style.display = 'none';
    }

    // 4. Gestion de l’envoi du formulaire pour ajouter une review.
    const reviewForm = document.getElementById('review-form');
    reviewForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // Récupération des valeurs remplies par l’utilisateur
        const reviewText = document.getElementById('review-text').value.trim();
        let rating = parseInt(document.getElementById('rating').value);

        // Vérification que la note est correcte : entre 0 et 5
        if (isNaN(rating) || rating < 0 || rating > 5) {
            alert('Rating must be a number between 0 and 5.');
            return;
        }

        // Appel de la fonction qui envoie les données à l'API.
        submitReview(token, placeId, reviewText, rating);
    });
});
