import zipfile
import os

files_to_zip = [
    'static/books/css/cart.css',
    'static/books/css/book_detail.css'
]

zip_filename = 'pustakam_update_patch.zip'

with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for file in files_to_zip:
        if os.path.exists(file):
            zipf.write(file)
            print(f"Added {file} to {zip_filename}")
        else:
            print(f"WARNING: File not found: {file}")

print(f"Created {zip_filename} successfully.")
