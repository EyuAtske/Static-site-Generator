from generatesite import generate_page, generate_pages_recursive
import re
import os
import shutil

def copy_static():
    parent_dir = os.path.dirname("static")
    public_dir = os.path.join(parent_dir, "public")
    static_dir = os.path.join(parent_dir, "static")
    shutil.rmtree(public_dir, ignore_errors=True)
    os.mkdir(public_dir)
    if os.path.exists(static_dir):
        all_files = os.listdir(static_dir)
        copy_files(public_dir, static_dir, all_files)
    else:
        raise FileNotFoundError("Static folder does not exist")
def copy_files(public, static, files):
    if len(files) == 0:
        return
    file_path = os.path.join(static, files[0])
    if os.path.isfile(file_path):
        destination = os.path.join(public, files[0])
        shutil.copy(file_path, destination)
        print(f"Copied {file_path} to {destination} folder")
        copy_files(public, static, files[1:])
    else:
        new_public = os.path.join(public, files[0])
        os.mkdir(new_public)
        print(f"Created folder: {new_public}")
        new_static = os.path.join(static, files[0])
        file = os.listdir(file_path)
        copy_files(new_public, new_static, file)

def main():
    copy_static()
    generate_pages_recursive("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()