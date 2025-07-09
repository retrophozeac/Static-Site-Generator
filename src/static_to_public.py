import os
import shutil

def static_to_public():
    if not os.path.exists("static"):
        raise Exception("Static folder not found")
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    recursive_copy("static","public")


def recursive_copy(src_dir, dest_dir):
    dirs = os.listdir(src_dir)
    for div in dirs:
        if os.path.isfile(os.path.join(src_dir,div)):
            shutil.copy(os.path.join(src_dir,div),os.path.join(dest_dir,div))
            print(f"Copying {os.path.join(src_dir,div)} to {os.path.join(dest_dir,div)}")
        else:
            os.mkdir(os.path.join(dest_dir,div))
            recursive_copy(os.path.join(src_dir,div),os.path.join(dest_dir,div))
    

    