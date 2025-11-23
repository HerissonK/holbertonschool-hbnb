// === UTILITY ===
// Fonction pour récupérer un cookie par son nom
// Utilisée pour lire le token JWT stocké lors du login
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// === AUTH CHECK ===
// Vérifie si l'utilisateur est connecté via le cookie "token"
// Gère l'affichage du bouton Login / Logout
// Et charge la liste des places en conséquence
function checkAuthentication() {
    const token = getCookie('token');
    const loginbutton = document.getElementById('login-button');
    const logoutButton = document.getElementById('logout-button');

    // Si pas connecté → afficher login, cacher logout, charger les places publiques
    if (!token) {
        if (loginbutton) loginbutton.style.display = 'inline-block';
        if (logoutButton) logoutButton.style.display = 'none';
        fetchPlaces(null); 
    } 
    // Si connecté → cacher login, afficher logout, charger les places accessibles via token
    else {
        if (loginbutton) loginbutton.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'inline-block';
        fetchPlaces(token);
    }
}

// === LOGOUT ===
// Supprime le cookie token + met à jour la page
function logout() {
    // Efface le cookie JWT
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    
    // Réaffichage des boutons
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-button');
    if (loginLink) loginLink.style.display = 'inline-block';
    if (logoutButton) logoutButton.style.display = 'none';

    // Recharge les places publiques
    fetchPlaces(null);
}

// === FETCH PLACES ===
// Récupère la liste des lieux depuis l'API
// Si un token est fourni → l'ajoute dans les headers
async function fetchPlaces(token) {
    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch('http://127.0.0.1:5000/api/v1/places/', { headers });

        if (!response.ok) throw new Error('Failed to fetch places');

        const places = await response.json();

        // Affiche les lieux
        displayPlaces(places);

        // Crée et initialise le filtre de prix
        populatePriceFilter();

    } catch (error) {
        console.error(error);
    }
}

// === DISPLAY PLACES ===
// Affiche dynamiquement chaque place dans la page
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = ''; // reset

    // Si aucun lieu trouvé
    if (!places || places.length === 0) {
        placesList.innerHTML = '<p>No places found.</p>';
        return;
    }

    // Création des cartes pour chaque lieu
    places.forEach(place => {
        const placeDiv = document.createElement('div');
        placeDiv.classList.add('place-card');
        placeDiv.setAttribute('data-price', place.price || 0);

        // Génération de la liste des amenities
        const amenitiesList = place.amenities && place.amenities.length
            ? place.amenities.map(a => a.name).join(', ')
            : 'No amenities';

        // Contenu de la carte
        placeDiv.innerHTML = `
            <h3>${place.title}</h3>
            <p><strong>Price per night:</strong> ${place.price ? place.price + ' €' : 'N/A'}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            <a href="add_review.html?id=${place.id}" class="add-review-link">Add Review</a>
        `;

        placesList.appendChild(placeDiv);
    });
}

// === FILTER ===
// Construit le menu déroulant pour filtrer par prix
function populatePriceFilter() {
    const filter = document.getElementById('price-filter');
    const options = [10, 50, 100, 'All'];
    filter.innerHTML = '';

    // Création des options du select
    options.forEach(value => {
        const option = document.createElement('option');
        option.value = value === 'All' ? '' : value;
        option.textContent = value === 'All' ? 'All' : `${value} €`;
        filter.appendChild(option);
    });

    // Ecouteur pour filtrer
    filter.addEventListener('change', handleFilterChange);
}

// Gère le filtrage des lieux en fonction du prix sélectionné
function handleFilterChange(event) {
    const maxPrice = event.target.value ? parseFloat(event.target.value) : Infinity;
    const cards = document.querySelectorAll('.place-card');
    const placesList = document.getElementById('places-list');

    let visibleCount = 0;

    // Affiche ou masque les cartes selon leur prix
    cards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price')) || 0;
        if (price <= maxPrice) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });

    // Vérifie si aucune carte n'est affichée
    const existingMessage = document.getElementById('no-results-message');

    if (visibleCount === 0) {
        if (!existingMessage) {
            const msg = document.createElement('p');
            msg.id = 'no-results-message';
            msg.textContent = 'No place correspond to your choices.';
            placesList.appendChild(msg);
        }
    } else {
        // Si des cartes existent, retire le message
        if (existingMessage) existingMessage.remove();
    }
}

// === INIT ===
// Fonction exécutée au chargement de la page
document.addEventListener('DOMContentLoaded', () => {

    // Vérifie l'authentification + charge les lieux
    checkAuthentication();

    // Ajout du comportement logout
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', logout);
    }
});
