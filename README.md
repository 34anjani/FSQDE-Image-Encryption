# 🔐 FSQDE – Fractal Swarm Based Quantum Diffusion Image Encryption Algorithm

## 📌 Overview

**FSQDE** is a Flask-based web application that encrypts and decrypts images using a multi-layered algorithm combining three sequential techniques: **Fractal permutation** using a logistic map for pixel shuffling, **Swarm noise injection** for adding controlled randomness and **Quantum XOR diffusion** for bit-level scrambling with neighboring pixels. Users upload an image through the browser and select **encryption strength** (Light, Balanced, or Extreme) after which the system produces an encrypted **PNG file and a password-protected key file** that must both be downloaded by the user. To decrypt, the user uploads the encrypted PNG along with the key file and enters the password which reverses all three encryption stages (Quantum, Swarm, Fractal) to recover the original image. After encryption, the app computes and **displays security metrics** including Entropy, NPCR, UACI, PSNR, Correlation, Chi-Square and APCC (Horizontal, Vertical, Diagonal) along with **histogram comparisons** of original vs encrypted images to verify randomness. All encryption records are stored in a **MySQL database** and can be viewed through the records endpoint providing a complete history of operations.

---
  
## 🔑 Key Features
**🧮 Multi-Layer Encryption Pipeline** - Applies three sequential encryption stages: Fractal shuffling, Swarm noise addition, and Quantum XOR diffusion for robust image protection.

**🔒 Password-Protected Key Management** - Encryption keys are secured using PBKDF2 + Fernet symmetric encryption, ensuring only the correct password can decrypt.

**📊 Security Metrics Dashboard** - Computes and displays Entropy, NPCR, UACI, PSNR, Correlation, Chi-Square, and APCC (Horizontal, Vertical, Diagonal) after every encryption.

**📈 Histogram Visualization** - Generates and compares pixel intensity histograms of original vs encrypted images for visual verification of randomness.

**⚡ Configurable Encryption Strength** - Three security modes: Light, Balanced, and Extreme, allowing users to control the noise intensity.

**🔓 Full Decryption Support** - Reverse the entire encryption pipeline using the encrypted image and key file to recover the original image.

---

## 🛠️ Technologies Used
- **⌨️ Python** – Core programming language
- **🌐 Flask** – Web framework for the backend
- **🔢 NumPy** – Numerical operations and pixel manipulation
- **🖼️ Pillow (PIL)** – Image loading and saving
- **📉 Matplotlib** – Histogram generation 
- **📐 SciPy** – Chi-square statistical analysis 
- **🔐 Cryptography (Fernet)** – Key file encryption
- **🗄️ MySQL** – Database for storing encryption records

---


## 📌 Use Case Scenarios
  - 🏥 **Medical Image Protection** – Encrypt sensitive patient scans and reports before sharing across hospital networks.
  - 🔬 **Research Data Confidentiality** – Secure proprietary research images and datasets from unauthorized access.
  - 🖼️ **Secure Image Transmission** – Safely transmit confidential images over untrusted channels using encryption keys.
  - 🎓 **Academic Cryptography Demonstration** – Understand and demonstrate chaos-based encryption techniques in academic projects.

---

## 🚀 How to Run
- **Prerequisites**
    - Python 3.x
    - MySQL needs to be installed and running.
- **Setup & Run**

1. Clone the repository
     ```bash
     git clone https://github.com/34anjani/FSQDE-Image-Encryption.git
     cd FSQDE-Image-Encryption
     ```
2. Install dependencies
     ```bash
     pip install flask numpy pillow matplotlib scipy cryptography mysql-connector-python
     ```
3. Set up the database
     ```bash
     mysql -u root -p < setup_db.sql
     ```
4. Run the application
     ```bash
     python app.py
     ```
5. Open http://127.0.0.1:5000 in your browser.
     - Upload and encrypt an image
     - Decrypt using encrypted image + key file
     - View all encryption history from database
