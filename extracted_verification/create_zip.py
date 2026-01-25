
import os
import zipfile

def zip_project(source_dir, output_filename):
    # Folders to exclude
    EXCLUDE_DIRS = {'.venv', 'venv', '.git', '__pycache__', 'staticfiles', '.idea', '.vscode'}
    # Files to exclude
    EXCLUDE_FILES = {'db.sqlite3', 'Pustakam_Final_Updated.zip'} # Safer to exclude local DB for production deployment

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if file in EXCLUDE_FILES or file.endswith('.pyc') or file.endswith('.zip'):
                    continue
                
                file_path = os.path.join(root, file)
                # Create a relative path for the archive to keep structure clean
                arcname = os.path.relpath(file_path, start=source_dir)
                zipf.write(file_path, arcname)
                print(f"Added: {arcname}")

if __name__ == "__main__":
    source = os.getcwd()
    output = "Pustakam_Final_Updated.zip"
    print(f"Zipping {source} to {output}...")
    zip_project(source, output)
    print("Done!")
