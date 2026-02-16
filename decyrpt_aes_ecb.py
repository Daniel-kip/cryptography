#!/usr/bin/env python3
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from PIL import Image
import numpy as np

def decrypt_image_ecb(encrypted_path, original_shape):
    # 1. Load the encrypted image and get the raw bytes
    enc_img = Image.open(encrypted_path).convert('RGB')
    enc_data = np.array(enc_img).tobytes()
    
    # 2. Setup the cipher (Must use the exact same key)
    key = b'sixteen_byte_key'
    cipher = AES.new(key, AES.MODE_ECB)
    
    # 3. Decrypt the data
    decrypted_padded = cipher.decrypt(enc_data)
    
    # 4. Remove padding
    # Note: ECB decryption requires the data to be a multiple of 16
    try:
        decrypted_final = unpad(decrypted_padded, AES.block_size)
    except ValueError:
        # If unpad fails (common if data was slightly altered), 
        # we manually slice to the expected size
        expected_size = original_shape[0] * original_shape[1] * original_shape[2]
        decrypted_final = decrypted_padded[:expected_size]

    # 5. Reshape and save
    decrypted_array = np.frombuffer(decrypted_final, dtype=np.uint8).reshape(original_shape)
    Image.fromarray(decrypted_array).save('decrypted_result.jpg')
    print("[+] Decryption complete: Check decrypted_result.jpg")

decrypt_image_ecb('ecb_encrypted.png', (1080, 1920, 3))
