import zipfile
import os

class AssetsOrganizer:
    def __init__(self):
        self.zip_path = 'assets.zip'
        self.extract_dir = 'test'

    def unzip_assets(self):
        if not os.path.exists(self.extract_dir):
            os.makedirs(self.extract_dir)

        if os.path.exists(self.zip_path):
            with zipfile.ZipFile(self.zip_path, 'r') as archive:
                archive.extractall(self.extract_dir)
        else:
            print(f"The zip file path {self.zip_path} doesn't exist")




if __name__ == '__main__':
    organizer = AssetsOrganizer()
    organizer.unzip_assets()

