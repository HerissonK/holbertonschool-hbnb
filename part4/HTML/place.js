// === UTILITY ===
// Récupère un cookie par son nom
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Récupère l'ID du lieu depuis l'URL
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

// === AUTH CHECK ===
// Vérifie si l'utilisateur est connecté
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-button');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        if (loginLink) loginLink.style.display = 'inline-block';
        if (addReviewSection) addReviewSection.style.display = 'none';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (addReviewSection) addReviewSection.style.display = 'block';
    }
    return token;
}

// === FETCH PLACE DETAILS ===
async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { headers });

        if (!response.ok) throw new Error('Failed to fetch place details');

        const place = await response.json();
        displayPlaceDetails(place);
        fetchPlaceReviews(placeId);
    } catch (error) {
        console.error(error);
        const detailsSection = document.getElementById('place-details');
        if (detailsSection) detailsSection.textContent = 'Failed to load place details.';
    }
}

// === DISPLAY PLACE DETAILS ===
function displayPlaceDetails(place) {
    const detailsSection = document.getElementById('place-details');
    if (!detailsSection) return;
    detailsSection.innerHTML = '';

    // Titre séparé
    const titleContainer = document.createElement('div');
    titleContainer.classList.add('place-title');
    const title = document.createElement('h2');
    title.textContent = place.title;
    titleContainer.appendChild(title);

    // Contenu du logement (hors titre)
    const detailsContainer = document.createElement('div');
    detailsContainer.classList.add('place-info');

    const host = document.createElement('p');
    host.innerHTML = `<strong>Host:</strong> ${place.owner_name || place.owner_id || 'Unknown'}`;

    const description = document.createElement('p');
    description.innerHTML = `<strong>Description:</strong> ${place.description || 'No description provided.'}`;

    const price = document.createElement('p');
    price.innerHTML = `<strong>Price per night:</strong> ${place.price} €`;

    const location = document.createElement('p');
    location.innerHTML = `<strong>Location:</strong> ${place.latitude}, ${place.longitude}`;

    const amenities = document.createElement('p');
    const amenitiesList = place.amenities && place.amenities.length
        ? place.amenities.map(a => a.name).join(', ')
        : 'No amenities';
    amenities.innerHTML = `<strong>Amenities:</strong> ${amenitiesList}`;

    detailsContainer.append(host, description, price, location, amenities);
    detailsSection.append(titleContainer, detailsContainer);
}

// === FETCH REVIEWS ===
async function fetchPlaceReviews(placeId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`);
        if (!response.ok) throw new Error('Failed to fetch reviews');
        const reviews = await response.json();
        displayReviews(reviews);
    } catch (error) {
        console.error(error);
        const reviewsSection = document.getElementById('reviews-list');
        if (reviewsSection) reviewsSection.innerHTML = '<p>Failed to load reviews.</p>';
    }
}

// === DISPLAY REVIEWS ===
function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews-list');
    if (!reviewsSection) return;
    reviewsSection.innerHTML = '<h3>Reviews</h3>';

    if (!reviews || reviews.length === 0) {
        reviewsSection.innerHTML += '<p>No reviews yet.</p>';
        return;
    }

    reviews.forEach(review => {
        const div = document.createElement('div');
        div.classList.add('review-card');

        const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);
        div.innerHTML = `
            <strong>${review.user_name || 'Anonymous'}</strong><br>
            ${review.text}<br>
            Rating: ${stars}
        `;
        reviewsSection.appendChild(div);
    });
}

// === HANDLE REVIEW FORM ===
function handleReviewForm(token, placeId) {
    const form = document.getElementById('review-form');
    if (!form) return;

    form.addEventListener('submit', async e => {
        e.preventDefault();
        const text = document.getElementById('review-text').value;
        const rating = parseInt(document.getElementById('review-rating').value);

        if (isNaN(rating) || rating < 0 || rating > 5) {
            alert('Rating must be between 0 and 5');
            return;
        }

        try {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ text, rating, place_id: placeId })
            });

            if (!response.ok) throw new Error('Failed to submit review');

            document.getElementById('review-text').value = '';
            fetchPlaceReviews(placeId);
        } catch (err) {
            alert(err.message);
        }
    });
}

// === INITIALIZE ===
document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (token) handleReviewForm(token, placeId);
    fetchPlaceDetails(token, placeId);
});
