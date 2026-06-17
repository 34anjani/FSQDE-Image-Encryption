import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request, send_from_directory
import numpy as np, os, time
from PIL import Image
import matplotlib.pyplot as plt
from encryption import *
from db import get_db

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)


@app.route("/", methods=["GET","POST"])
def upload_encrypt():
    if request.method == "POST":
        file = request.files["image"]
        password = request.form["password"]
        mode = request.form["mode"]

        strength_map = {"Light":64, "Balanced":128, "Extreme":256}
        strength = strength_map[mode]

        # Load image
        img = np.array(Image.open(file).convert("RGB"), dtype=np.uint8)

        # Save original image for display
        Image.fromarray(img).save("static/original.png")

        seed = int.from_bytes(password.encode(),"big") % 1000000
        x = (seed % 1000) / 1000

        # -------- Encryption Time --------
        start_time = time.time()

        f_img, idx = fractal_encrypt(img, x)
        s_img, noise = swarm_encrypt(f_img, seed, strength)
        encrypted = quantum_diffuse(s_img)

        encrypted = np.clip(encrypted, 0, 255).astype(np.uint8)

        enc_time = time.time() - start_time
        # ---------------------------------

        keydata = encrypt_key_file(idx, noise, password)

        # -------- Metrics --------
        entropy = calculate_entropy(encrypted)
        npcr, uaci = calculate_npcr_uaci(img, encrypted)
        psnr = calculate_psnr(img, encrypted)
        corr = calculate_correlation(img, encrypted)
        chi = calculate_chi_square(encrypted)
        apcc_h, apcc_v, apcc_d = calculate_apcc(img, encrypted)
        # -------------------------

        # -------- Histograms --------
        plt.figure()
        plt.hist(img.flatten(), bins=256, color="blue")
        plt.title("Histogram of Original Image")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        plt.savefig("static/hist_original.png")
        plt.close()

        plt.figure()
        plt.hist(encrypted.flatten(), bins=256, color="red")
        plt.title("Histogram of Encrypted Image")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        plt.savefig("static/hist_encrypted.png")
        plt.close()
        # ----------------------------

        # Save images for display
        Image.fromarray(encrypted).save("static/encrypted.png")

        # Save files for download
        Image.fromarray(encrypted).save("uploads/encrypted.png")
        with open("uploads/fsqde_key.enc","wb") as f:
            f.write(keydata)

        # Save to database
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO images(
        filename,
        entropy, npcr, uaci, psnr, correlation, chi_square,
        encryption_time, decryption_time,
        apcc_h, apcc_v, apcc_d
        )
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            file.filename,
            entropy, npcr, uaci, psnr, corr, chi,
            enc_time, 0,
            apcc_h, apcc_v, apcc_d
        ))

        conn.commit()
        conn.close()

        return render_template(
            "result.html",
            entropy=entropy,
            npcr=npcr,
            uaci=uaci,
            psnr=psnr,
            corr=corr,
            chi=chi,
            apcc_h=apcc_h,
            apcc_v=apcc_v,
            apcc_d=apcc_d,
            enc_time=enc_time
        )

    return render_template("upload.html")


@app.route("/decrypt", methods=["GET","POST"])
def decrypt():
    if request.method == "POST":
        enc_img = request.files["enc_image"]
        key_file = request.files["key_file"]
        password = request.form["password"]

        enc = np.array(Image.open(enc_img).convert("RGB"), dtype=np.uint8)
        keydata = decrypt_key_file(key_file.read(), password)
        idx, noise = keydata["indices"], keydata["noise"]

        # -------- Decryption Time --------
        start_time = time.time()

        r1 = reverse_quantum_diffuse(enc)
        r2 = swarm_decrypt(r1, noise)
        dec = fractal_decrypt(r2, idx)

        dec = np.clip(dec, 0, 255).astype(np.uint8)

        dec_time = time.time() - start_time
        # ---------------------------------

        # Update last record safely
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        UPDATE images
        SET decryption_time=%s
        WHERE id = (SELECT MAX(id) FROM (SELECT id FROM images) AS tmp)
        """, (dec_time,))
        conn.commit()
        conn.close()

        Image.fromarray(dec).save("static/decrypted.png")
        Image.fromarray(dec).save("uploads/decrypted.png")

        return render_template("decrypt_result.html", dec_time=dec_time)

    return render_template("decrypt.html")


# -------- DOWNLOAD ROUTES --------
@app.route("/download/encrypted")
def download_encrypted():
    return send_from_directory("uploads", "encrypted.png", as_attachment=True)

@app.route("/download/key")
def download_key():
    return send_from_directory("uploads", "fsqde_key.enc", as_attachment=True)

@app.route("/download/decrypted")
def download_decrypted():
    return send_from_directory("uploads", "decrypted.png", as_attachment=True)
# --------------------------------


@app.route("/records")
def records():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM images")
    rows = cur.fetchall()
    conn.close()
    return render_template("records.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)