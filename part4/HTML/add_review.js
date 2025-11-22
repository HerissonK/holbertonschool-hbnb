// === UTILITY ===
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// === CHECK AUTHENTICATION ===
function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        alert('You must be logged in to add a review.');
        window.location.href = 'login.html';
    }
    return token;
}

// === GET PLACE ID FROM URL ===
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// === SUBMIT REVIEW ===
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: rating,
                place_id: placeId
            })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Failed to submit review');
        }

        alert('Review submitted successfully!');
        window.location.href = `place.html?id=${placeId}`; // redirection vers la page détail
    } catch (error) {
        alert('Error submitting review: ' + error.message);
    }
}

// === EVENT LISTENER ===
document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    // === HIDE LOGIN BUTTON IF USER IS AUTHENTICATED ===
    const loginLink = document.getElementById('login-link');
    if (token && loginLink) {
        loginLink.style.display = 'none';
    }

    const reviewForm = document.getElementById('review-form');
    reviewForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const reviewText = document.getElementById('review-text').value.trim();
        let rating = parseInt(document.getElementById('rating').value);
        if (isNaN(rating) || rating < 0 || rating > 5) {
            alert('Rating must be a number between 0 and 5.');
            return;
        }

        submitReview(token, placeId, reviewText, rating);
    });
});
