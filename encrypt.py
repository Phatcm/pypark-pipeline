from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
import hashlib


class Encryptor:
    def __init__(self, password):
        self.password = password
        self.buffer_size = 65536 # 64kb
        
    def create_key(self):
        salt = b'\xa4\xb0\x80H\xae\xaa\xf8\xcbK\x10\x8ej\xcdA\xc3\xf0\xebqtr\x92\x87\x12x/I\xddQ,J\xd3\x16'
        key = PBKDF2(self.password, salt, dkLen=32)
        return key
    
    def encrypt_file(self, file_to_encrypt):
        # Open the input and output files
        input_file = open(file_to_encrypt, 'rb')
        output_file = open(file_to_encrypt + '.encrypted', 'wb')
        
        # Create the cipher object and encrypt the data
        cipher_encrypt = AES.new(self.create_key(), AES.MODE_CFB)
        # Initially write the iv to the output file
        output_file.write(cipher_encrypt.iv)
        
        # Keep reading the file into the buffer, encrypting then writing to the new file
        buffer = input_file.read(self.buffer_size)
        while len(buffer) > 0:
            ciphered_bytes = cipher_encrypt.encrypt(buffer)
            output_file.write(ciphered_bytes)
            buffer = input_file.read(self.buffer_size)
        
        input_file.close()
        output_file.close()
    
    def decrypt_file(self, file_to_decrypt):
        input_file = open(file_to_decrypt + '.encrypted', 'rb')
        output_file = open(file_to_decrypt + '.decrypted', 'wb')
        
        # Read in the iv
        iv = input_file.read(16)
        # Create the cipher object and encrypt the data
        cipher_encrypt = AES.new(self.create_key(), AES.MODE_CFB, iv=iv)
        
        # Keep reading the file into the buffer, decrypting then writing to the new file
        buffer = input_file.read(self.buffer_size)
        while len(buffer) > 0:
            decrypted_bytes = cipher_encrypt.decrypt(buffer)
            output_file.write(decrypted_bytes)
            buffer = input_file.read(self.buffer_size)
        
        input_file.close()
        output_file.close()
        

    def get_file_hash(self,file_path):
        block_size = 65536
        file_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            fb = f.read(block_size)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(block_size)
        return file_hash.hexdigest()
