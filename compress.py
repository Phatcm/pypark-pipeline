import os 
import zipfile

class Compressor:
    def __init__(self, path):
        self.path = path
        
    def compress_all_files(self, zipname):
        zip = zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED)
        for dirname, subdirs, files in os.walk(self.path):
            zip.write(dirname)
            for filename in files:
                zip.write(os.path.join(dirname, filename))
        zip.close()
    
    def decompress_file(self, zipname):
        zip = zipfile.ZipFile(zipname, "r")
        zip.extractall()
        zip.close()
        
        
