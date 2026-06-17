import numpy as np, io, os, base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from scipy.stats import chisquare
import matplotlib.pyplot as plt

def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_key_file(indices, noise, password):
    salt = os.urandom(16)
    key = derive_key(password, salt)
    fernet = Fernet(key)
    buf = io.BytesIO()
    np.savez_compressed(buf, indices=indices, noise=noise)
    return salt + fernet.encrypt(buf.getvalue())

def decrypt_key_file(data, password):
    salt, encrypted = data[:16], data[16:]
    key = derive_key(password, salt)
    decrypted = Fernet(key).decrypt(encrypted)
    return np.load(io.BytesIO(decrypted))

def logistic_map(x):
    return 3.99*x*(1-x)

def fractal_encrypt(img, x):
    h,w,c = img.shape
    seq = [logistic_map(x:=logistic_map(x)) for _ in range(h*w)]
    idx = np.argsort(np.array(seq).reshape(h,w), axis=1)
    out = np.zeros_like(img)
    for i in range(h):
        for ch in range(c):
            out[i,:,ch] = img[i,idx[i],ch]
    return out, idx

def fractal_decrypt(img, idx):
    out = np.zeros_like(img)
    for i in range(img.shape[0]):
        for ch in range(3):
            out[i,idx[i],ch] = img[i,:,ch]
    return out

def swarm_encrypt(img, seed, strength):
    np.random.seed(seed)
    noise = np.random.randint(0,strength,img.shape,dtype=np.uint8)
    return ((img.astype(np.uint16)+noise)%256).astype(np.uint8), noise

def swarm_decrypt(img, noise):
    return ((img.astype(np.uint16)-noise+256)%256).astype(np.uint8)

def quantum_diffuse(img):
    out = img.copy()
    h,w,_ = img.shape
    for i in range(h):
        for j in range(w):
            out[i,j] ^= out[(i+1)%h,j] ^ out[i,(j+1)%w]
    return out

def reverse_quantum_diffuse(img):
    out = img.copy()
    h,w,_ = img.shape
    for i in reversed(range(h)):
        for j in reversed(range(w)):
            out[i,j] ^= out[(i+1)%h,j] ^ out[i,(j+1)%w]
    return out

def calculate_entropy(image):
    hist,_ = np.histogram(image,bins=256,range=(0,255))
    prob = hist/np.sum(hist)
    return -np.sum([p*np.log2(p) for p in prob if p>0])

def calculate_npcr_uaci(img1,img2):
    diff = img1!=img2
    npcr = np.sum(diff)/diff.size*100
    uaci = np.mean(np.abs(img1.astype(int)-img2.astype(int))/255)*100
    return npcr,uaci

def calculate_psnr(img1,img2):
    mse = np.mean((img1-img2)**2)
    return float("inf") if mse==0 else 20*np.log10(255/np.sqrt(mse))

def calculate_correlation(img1,img2):
    return np.corrcoef(img1.flatten(),img2.flatten())[0,1]

def calculate_chi_square(image):
    gray = image.mean(axis=2).astype(np.uint8)
    hist,_ = np.histogram(gray,bins=256,range=(0,256))
    expected = np.ones_like(hist)*(np.sum(hist)/256)
    chi,_ = chisquare(hist,f_exp=expected)
    return chi

import numpy as np

def calculate_apcc(original, encrypted):
    # Horizontal, Vertical, Diagonal correlations
    H = np.corrcoef(original[:, :-1].flatten(), encrypted[:, 1:].flatten())[0,1]
    V = np.corrcoef(original[:-1, :].flatten(), encrypted[1:, :].flatten())[0,1]
    D = np.corrcoef(original[:-1, :-1].flatten(), encrypted[1:, 1:].flatten())[0,1]
    return H, V, D

