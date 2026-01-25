import zipfile
import os

def create_patch():
    file_to_patch = 'templates/books/register.html'
    zip_name = 'pustakam_fix.zip'
    
    if not os.path.exists(file_to_patch):
        print(f"Error: {file_to_patch} not found!")
        return

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        print(f"Adding {file_to_patch} to {zip_name}...")
        zipf.write(file_to_patch)
        
    print(f"Success! Created {zip_name}")
    print("Instructions:")
    print(f"1. Upload {zip_name} to PythonAnywhere (inside your project folder).")
    print(f"2. Run: unzip -o {zip_name}")
    print("3. Reload your Web App.")

if __name__ == '__main__':
    create_patch()
