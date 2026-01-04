from generatesite import generate_page, generate_pages_recursive
import re
import os
import shutil
import sys

def copy_static(basepath):
    static_dir = "./static"
    shutil.rmtree(basepath, ignore_errors=True)
    os.mkdir(basepath)
    if os.path.exists(static_dir):
        all_files = os.listdir(static_dir)
        copy_files(basepath, static_dir, all_files)
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
    basepath = ""
    output_dir = "./docs"
    if len(sys.argv) != 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    copy_static(output_dir)
    generate_pages_recursive("./content", "./template.html", output_dir, basepath)

if __name__ == "__main__":
    main()