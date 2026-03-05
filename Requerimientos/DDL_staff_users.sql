-- Query para crear la tabla de usuarios del staff en edwared_master
-- Ejecutar en pgAdmin4 conectado a edwared_master

CREATE TABLE IF NOT EXISTS staff_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    whatsapp VARCHAR(20),
    fecha_nacimiento DATE,
    password_hash VARCHAR(256),
    pin_rapido VARCHAR(10),
    cargo VARCHAR(100),
    nivel_etiqueta VARCHAR(50) DEFAULT 'User',
    nivel_numerico INTEGER DEFAULT 50,
    antiguedad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Index para búsqueda rápida por username
CREATE INDEX IF NOT EXISTS ix_staff_users_username ON staff_users (username);

-- Insertar usuario administrador inicial (password: admin123 - HASHEADO)
-- Nota: En producción esto se debe cambiar inmediatamente
INSERT INTO staff_users (username, nombres, apellidos, nivel_etiqueta, nivel_numerico, cargo)
VALUES ('edwared_admin', 'Admin', 'Sistema', 'Super Admin', 100, 'Director')
ON CONFLICT (username) DO NOTHING;
