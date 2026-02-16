#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from PIL import Image
import numpy as np

def encrypt_image_ecb(input_path):
    # 1. Open image and convert to RGB (to ensure 3 channels)
    img = Image.open(input_path).convert('RGB')
    img_data = np.array(img)
    shape = img_data.shape
    
    # Changing it to bytes
    flat = img_data.tobytes()
    
    # 2. Key must be EXACTLY 16, 24, or 32 bytes
    key = b'sixteen_byte_key' 
    cipher = AES.new(key, AES.MODE_ECB)
    
    # 3. Pad to block size (16)
    #This is just an additional measure 
    padded = pad(flat, AES.block_size)
    encrypted = cipher.encrypt(padded)
    
    # 4. Truncate padding to fit original dimensions for reshaping
    # Note: For visual ECB effect, we map back to the original byte length
    encrypted_data = np.frombuffer(encrypted[:len(flat)], dtype=np.uint8)
    encrypted_img = encrypted_data.reshape(shape)
    
    # 5. Save output
    Image.fromarray(encrypted_img).save('ecb_encrypted.png')
    print("[!] ECB Mode: Done. Check ecb_encrypted.png")

# run it:
encrypt_image_ecb('image.jpg')
