CREATE DATABASE IF NOT EXISTS fsqde;
CREATE USER IF NOT EXISTS 'fsqdeuser'@'localhost' IDENTIFIED BY 'fsqde123';
GRANT ALL PRIVILEGES ON fsqde.* TO 'fsqdeuser'@'localhost';
FLUSH PRIVILEGES;
USE fsqde;

CREATE TABLE IF NOT EXISTS images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    encrypted_image LONGBLOB,
    key_file BLOB,
    entropy FLOAT,
    npcr FLOAT,
    uaci FLOAT,
    psnr FLOAT,
    correlation FLOAT,
    chi_square FLOAT,
    encryption_time FLOAT,
    decryption_time FLOAT,
    apcc_h FLOAT,
    apcc_v FLOAT,
    apcc_d FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
