import os
import urllib.request
import zipfile
from tqdm import tqdm

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True, 
                           miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def main():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    coco_dir = os.path.join(data_dir, 'coco')
    os.makedirs(coco_dir, exist_ok=True)
    
    # Annotations only (smaller)
    annotations_url = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'
    annotations_zip = os.path.join(coco_dir, "annotations.zip")
    
    if not os.path.exists(os.path.join(coco_dir, "annotations")):
        print(f"Downloading annotations...")
        download_url(annotations_url, annotations_zip)
        print(f"Extracting annotations...")
        with zipfile.ZipFile(annotations_zip, 'r') as zip_ref:
            zip_ref.extractall(coco_dir)
    
    print("Would you like to download images? (Warning: large files)")
    print("1: Download validation set only (~1GB)")
    print("2: Download full training set (~18GB)")
    print("3: Skip image download")
    
    choice = input("Enter choice (1/2/3): ")
    
    if choice == "1" or choice == "2":
        val_url = 'http://images.cocodataset.org/zips/val2017.zip'
        val_zip = os.path.join(coco_dir, "val2017.zip")
        if not os.path.exists(os.path.join(coco_dir, "val2017")):
            print(f"Downloading validation images...")
            download_url(val_url, val_zip)
            print(f"Extracting validation images...")
            with zipfile.ZipFile(val_zip, 'r') as zip_ref:
                zip_ref.extractall(coco_dir)
    
    if choice == "2":
        train_url = 'http://images.cocodataset.org/zips/train2017.zip'
        train_zip = os.path.join(coco_dir, "train2017.zip")
        if not os.path.exists(os.path.join(coco_dir, "train2017")):
            print(f"Downloading training images...")
            download_url(train_url, train_zip)
            print(f"Extracting training images...")
            with zipfile.ZipFile(train_zip, 'r') as zip_ref:
                zip_ref.extractall(coco_dir)
    
    print("Dataset setup complete!")

if __name__ == "__main__":
    main()