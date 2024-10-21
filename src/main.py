from helper_functions import *
import os
import shutil

dir_path_static = "static"
dir_path_public = "public"
dir_path_content = "content"
template_path = "./template.html"
    

def main():
    print("Deleting public directory...")
    # Step 1: Delete all contents in the destination directory
    delete_destination_contents(dir_path_public)
    
    # Step 2: Copy all contents from the source to the destination
    print("Copying static files to public directory...")
    copy_directory_recursive(dir_path_static, dir_path_public)
    
    # Step 3: Generate the webpage
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)
       
main()