# 🔐 FSQDE – Fractal Swarm Quantum Diffusion Image Encryption
  
  FSQDE is a Flask-based image encryption system that applies a multi-layered
  encryption algorithm combining Fractal permutation, Swarm noise injection, and
  Quantum Diffusion techniques. It provides comprehensive security metrics analysis
  to evaluate encryption strength.
  
**🔑 Key Features**
- 🧮 Multi-Layer Encryption Pipeline : Applies three sequential encryption stages: Fractal shuffling, Swarm noise addition, and Quantum XOR diffusion for robust image protection.
- 🔒 Password-Protected Key Management : Encryption keys are secured using PBKDF2 + Fernet symmetric encryption, ensuring only the correct password can decrypt.
- 📊 Security Metrics Dashboard : Computes and displays Entropy, NPCR, UACI, PSNR, Correlation, Chi-Square, and APCC (Horizontal, Vertical, Diagonal) after every encryption.
- 📈 Histogram Visualization : Generates and compares pixel intensity histograms of original vs encrypted images for visual verification of randomness.
- ⚡ Configurable Encryption Strength : Three security modes: Light, Balanced, and Extreme, allowing users to control the noise intensity.
- 🔓 Full Decryption Support : Reverse the entire encryption pipeline using the encrypted image and key file to recover the original image.
  
**🛠️ Technologies Used**
- ⌨️ Python – Core programming language
- 🌐 Flask – Web framework for the backend
- 🔢 NumPy – Numerical operations and pixel manipulation
- 🖼️ Pillow (PIL) – Image loading and saving
- 📉 Matplotlib – Histogram generation 
- 📐 SciPy – Chi-square statistical analysis 
- 🔐 Cryptography (Fernet) – Key file encryption
- 🗄️ MySQL – Database for storing encryption records
    
**📌 Use Case Scenarios**
- 🏥 Medical Image Protection
- 🔬 Research Data Confidentiality
- 🖼️ Secure Image Transmission
- 🎓 Academic Cryptography Demonstration
  
**🚀 How to Run**
- Prerequisites
    - Python 3.x
    - MySQL installed and running
- Setup & Run
    1. Clone the repository
      git clone https://github.com/34anjani/FSQDE-Image-Encryption.git
      cd FSQDE-Image-Encryption
    2. Install dependencies
      pip install flask numpy pillow matplotlib scipy cryptography mysql-connector-python
    3. Set up the database
      mysql -u root -p < setup_db.sql
    4. Run the application
      python app.py
    5. Open http://127.0.0.1:5000 in your browser.
      - / – Upload and encrypt an image
      - /decrypt – Decrypt using encrypted image + key file
      - /records – View all encryption history from database
