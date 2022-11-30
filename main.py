from compress import Compressor
from encrypt import Encryptor
import database
import os
import pysftp




def main(dir):
    while len(dir) != 0:
        choice = int(input("""
                           1. Press '1' to compress.\n
                           2. Press '2' to encrypt.\n
                           3. Press '3' to upload data to sftp.\n
                           4. Press '4' to download data from sftp.\n
                           5. Press '5' to decompress and decrypt.\n
                           6. Press '6' to create database.\n
                           7. Press '7' to run ETL process"""))
        if choice == 1:
            try:
                c = Compressor(path)
                c.compress_all_files('data.zip')
            except:
                print("Failed to compress file!\n")
        elif choice == 2:
            try:
                password = input("Enter password: ")
                e = Encryptor(password)
                e.encrypt_file(zipfile)
            except:
                print("Something were wrong when encrypt file!\n")
        elif choice == 3:
            with pysftp.Connection(host=sftpHost, port=sftpPort, username=uname, private_key=privateKeyFilePath, cnopts=cnopts) as sftp:
                print('Connected to sftp server')
                sftp.cwd("C:/remFolder")

                #Only compress is require, encrypt file is optional
                try:
                    sftp.put(zipenc,preserve_mtime=True)
                    print("Send data.zip.encrypted")
                    break
                except:
                    sftp.put(zipfile,preserve_mtime=True)
                    print("Send data.zip")
        elif choice == 4:
            with pysftp.Connection(host=sftpHost, port=sftpPort, username=uname, private_key=privateKeyFilePath, cnopts=cnopts) as sftp:
                print('Connected to sftp server')
                sftp.cwd("C:/remFolder")

                try:
                    sftp.get(zipenc,preserve_mtime=True)
                    print("Get data.zip.encrypted")
                    break
                except:
                    sftp.get(zipfile,preserve_mtime=True)
                    print("Get data.zip")
        elif choice == 5:
            try:
                c = Compressor("./")
                c.decompress_file('data.zip')
            except:
                password = input("Enter password: ")
                e = Encryptor(password)
                e.decrypt_file(zipfile)
                
                c = Compressor("./")
                c.decompress_file(zipdec)
        elif choice == 6:
            try:
                database.main()
                print("Create starschema successfully")
            except:
                print("Something were wrong when create starschema")
        elif choice == 7:
            print("In progress")
        
                
                
            
if __name__ == '__main__':
    #Direction setup
    current = "./"
    path = "data/"
    zipfile = path[0:-1]+".zip"
    zipenc = zipfile+".encrypted"
    zipdec = zipfile+".decrypted"
    dir = os.listdir(current)
    
    #Postgresql setup
    sftpHost = 'localhost'
    sftpPort = 22
    uname = 'Admin'
    privateKeyFilePath = './id_rsa'
    cnopts = pysftp.CnOpts(knownhosts=r'C:\Users\Admin\.ssh\known_hosts')
    
    main(dir)



#check hash
#assert e.get_file_hash(file) == e.get_file_hash(file + '.decrypted'), 'Files are not identical'

