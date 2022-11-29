from compress import Compressor
from encrypt import Encryptor


# Compress all files in data directory
path = "data/"
c = Compressor(path)
#c.compress_all_files('data.zip')


# Encrypt data.zip with AES encryption
file = "data.zip"
password = input("Enter password: ")
e = Encryptor(password)
#e.encrypt_file(file)

#e.decrypt_file(file)


#check hash
#assert e.get_file_hash(file) == e.get_file_hash(file + '.decrypted'), 'Files are not identical'

