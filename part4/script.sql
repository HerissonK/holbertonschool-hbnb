-- =====================================================
-- Script SQL pour la base de données HBnB
-- Création des tables et initialisation des données
-- =====================================================

-- Suppression de la base de données si elle existe déjà
DROP DATABASE IF EXISTS hbnb;

-- Création de la base de données
CREATE DATABASE hbnb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Utilisation de la base de données
USE hbnb;

-- =====================================================
-- CRÉATION DES TABLES
-- =====================================================

-- Table User
CREATE TABLE User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table Place
CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

-- Table Amenity
CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table Review
CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_place_review (user_id, place_id)
);

-- Table Place_Amenity (relation many-to-many)
CREATE TABLE Place_Amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id) ON DELETE CASCADE
);

-- =====================================================
-- INDEX POUR OPTIMISATION
-- =====================================================

CREATE INDEX idx_place_owner ON Place(owner_id);
CREATE INDEX idx_review_user ON Review(user_id);
CREATE INDEX idx_review_place ON Review(place_id);
CREATE INDEX idx_user_email ON User(email);

-- =====================================================
-- INSERTION DES DONNÉES INITIALES
-- =====================================================

-- Insertion de l'utilisateur administrateur
-- Mot de passe: admin1234
-- Hash bcrypt: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ajikJVq5W6Zi
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ajikJVq5W6Zi',
    TRUE
);

-- Insertion des équipements (amenities) initiaux
INSERT INTO Amenity (id, name) VALUES
    ('a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d', 'WiFi'),
    ('b2c3d4e5-f6a7-4b5c-9d0e-1f2a3b4c5d6e', 'Swimming Pool'),
    ('c3d4e5f6-a7b8-4c5d-0e1f-2a3b4c5d6e7f', 'Air Conditioning');

-- =====================================================
-- VÉRIFICATION DES DONNÉES INSÉRÉES
-- =====================================================

-- Affichage de l'utilisateur admin
SELECT 'Utilisateur Administrateur:' AS '';
SELECT id, first_name, last_name, email, is_admin, created_at 
FROM User 
WHERE is_admin = TRUE;

-- Affichage des équipements
SELECT '' AS '';
SELECT 'Équipements (Amenities):' AS '';
SELECT id, name, created_at 
FROM Amenity 
ORDER BY name;

-- =====================================================
-- EXEMPLES DE TESTS CRUD
-- =====================================================

-- Test 1: Création d'un utilisateur standard
SELECT '' AS '';
SELECT 'Test 1: Création d\'un utilisateur standard' AS '';
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES (
    'f47ac10b-58cc-4372-a567-0e02b2c3d479',
    'Jean',
    'Dupont',
    'jean.dupont@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ajikJVq5W6Zi',
    FALSE
);
SELECT id, first_name, last_name, email, is_admin FROM User WHERE email = 'jean.dupont@example.com';

-- Test 2: Création d'une place
SELECT '' AS '';
SELECT 'Test 2: Création d\'une place (logement)' AS '';
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    'e47ac10b-58cc-4372-a567-0e02b2c3d480',
    'Appartement Paris Centre',
    'Magnifique appartement au coeur de Paris',
    120.50,
    48.8566,
    2.3522,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
);
SELECT id, title, description, price, owner_id FROM Place WHERE id = 'e47ac10b-58cc-4372-a567-0e02b2c3d480';

-- Test 3: Association d'équipements à une place
SELECT '' AS '';
SELECT 'Test 3: Association d\'équipements à la place' AS '';
INSERT INTO Place_Amenity (place_id, amenity_id)
VALUES 
    ('e47ac10b-58cc-4372-a567-0e02b2c3d480', 'a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d'),
    ('e47ac10b-58cc-4372-a567-0e02b2c3d480', 'c3d4e5f6-a7b8-4c5d-0e1f-2a3b4c5d6e7f');

SELECT p.title, a.name
FROM Place p
JOIN Place_Amenity pa ON p.id = pa.place_id
JOIN Amenity a ON pa.amenity_id = a.id
WHERE p.id = 'e47ac10b-58cc-4372-a567-0e02b2c3d480';

-- Test 4: Création d'un avis (review)
SELECT '' AS '';
SELECT 'Test 4: Création d\'un avis' AS '';
INSERT INTO Review (id, text, rating, user_id, place_id)
VALUES (
    'd47ac10b-58cc-4372-a567-0e02b2c3d481',
    'Excellent séjour, appartement très bien situé!',
    5,
    'f47ac10b-58cc-4372-a567-0e02b2c3d479',
    'e47ac10b-58cc-4372-a567-0e02b2c3d480'
);
SELECT r.text, r.rating, u.first_name, u.last_name, p.title
FROM Review r
JOIN User u ON r.user_id = u.id
JOIN Place p ON r.place_id = p.id
WHERE r.id = 'd47ac10b-58cc-4372-a567-0e02b2c3d481';

-- Test 5: Mise à jour d'un utilisateur
SELECT '' AS '';
SELECT 'Test 5: Mise à jour d\'un utilisateur' AS '';
UPDATE User 
SET first_name = 'Jean-Pierre' 
WHERE email = 'jean.dupont@example.com';
SELECT first_name, last_name, email FROM User WHERE email = 'jean.dupont@example.com';

-- Test 6: Suppression d'un avis
SELECT '' AS '';
SELECT 'Test 6: Suppression d\'un avis' AS '';
DELETE FROM Review WHERE id = 'd47ac10b-58cc-4372-a567-0e02b2c3d481';
SELECT COUNT(*) AS nombre_avis FROM Review WHERE id = 'd47ac10b-58cc-4372-a567-0e02b2c3d481';

-- =====================================================
-- RÉSUMÉ FINAL
-- =====================================================

SELECT '' AS '';
SELECT '=====================================================' AS '';
SELECT 'RÉSUMÉ DE LA BASE DE DONNÉES' AS '';
SELECT '=====================================================' AS '';

SELECT CONCAT('Nombre d\'utilisateurs: ', COUNT(*)) AS stat FROM User
UNION ALL
SELECT CONCAT('Nombre de places: ', COUNT(*)) FROM Place
UNION ALL
SELECT CONCAT('Nombre d\'équipements: ', COUNT(*)) FROM Amenity
UNION ALL
SELECT CONCAT('Nombre d\'avis: ', COUNT(*)) FROM Review;

SELECT '' AS '';
SELECT 'Base de données HBnB créée et initialisée avec succès!' AS '';
SELECT '=====================================================' AS '';