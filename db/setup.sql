CREATE DATABASE ax_health;
USE ax_health;

-- TABLE 1: Patient Records (real users)
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    fever INT,
    cough INT,
    headache INT,
    fatigue INT,
    risk_level VARCHAR(20)
);

-- TABLE 2: ML Training Data (dataset)
CREATE TABLE ml_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    age INT,
    fever INT,
    cough INT,
    headache INT,
    fatigue INT,
    disease VARCHAR(50)
);

INSERT INTO ml_data (age, fever, cough, headache, fatigue, disease) VALUES
(25, 1, 1, 0, 1, 'Flu'),
(60, 1, 1, 1, 1, 'Viral Infection'),
(45, 0, 1, 1, 0, 'Migraine'),
(30, 0, 0, 0, 0, 'Healthy'),
(70, 1, 1, 1, 1, 'Critical Infection'),
(50, 1, 0, 1, 1, 'Flu');

