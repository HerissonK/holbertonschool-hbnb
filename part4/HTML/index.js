// === UTILITY ===
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// === AUTH CHECK ===
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');

    if (!token) {
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutButton) logoutButton.style.display = 'none';
        fetchPlaces(null);
    } else {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'inline-block';
        fetchPlaces(token);
    }
}

// === LOGOUT ===
function logout() {
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');

    if (loginLink) loginLink.style.display = 'inline-block';
    if (logoutButton) logoutButton.style.display = 'none';

    fetchPlaces(null);
}

// === FETCH PLACES ===
async function fetchPlaces(token) {
    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', { headers });
        if (!response.ok) throw new Error('Failed to fetch places');

        const places = await response.json();
        displayPlaces(places);
        populatePriceFilter();
    } catch (error) {
        console.error(error);
    }
}

// === DISPLAY PLACES ===
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places found.</p>';
        return;
    }

    places.forEach(place => {
        const placeDiv = document.createElement('div');
        placeDiv.classList.add('place-card');
        placeDiv.setAttribute('data-price', place.price || 0);

        const amenitiesList = place.amenities && place.amenities.length
            ? place.amenities.map(a => a.name).join(', ')
            : 'No amenities';

        placeDiv.innerHTML = `
            <h3>${place.title}</h3>
            <p>${place.description || 'No description provided.'}</p>
            <p><strong>Price:</strong> ${place.price ? place.price + ' €' : 'N/A'}</p>
            <p><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
            <p><strong>Amenities:</strong> ${amenitiesList}</p>
            <a href="place.html?id=${place.id}" class="details-link">View Details</a>
            <a href="add_review.html?id=${place.id}" class="add-review-link">Add Review</a>
        `;

        placesList.appendChild(placeDiv);
    });
}

// === FILTER ===
function populatePriceFilter() {
    const filter = document.getElementById('price-filter');
    const options = ['All', 50, 100, 150, 200];
    filter.innerHTML = '';

    options.forEach(value => {
        const option = document.createElement('option');
        option.value = value === 'All' ? '' : value;
        option.textContent = value === 'All' ? 'All' : `${value} €`;
        filter.appendChild(option);
    });

    filter.addEventListener('change', handleFilterChange);
}

function handleFilterChange(event) {
    const maxPrice = event.target.value ? parseFloat(event.target.value) : Infinity;
    const cards = document.querySelectorAll('.place-card');
    const placesList = document.getElementById('places-list');

    let visibleCount = 0;

    cards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price')) || 0;
        if (price <= maxPrice) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });

    // === If no visible card, show message ===
    const existingMessage = document.getElementById('no-results-message');

    if (visibleCount === 0) {
        if (!existingMessage) {
            const msg = document.createElement('p');
            msg.id = 'no-results-message';
            msg.textContent = 'No place correspond to your choices.';
            msg.style.textAlign = 'center';
            msg.style.marginTop = '20px';
            placesList.appendChild(msg);
        }
    } else {
        if (existingMessage) existingMessage.remove();
    }
}

// === INIT ===
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();

    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }
});
