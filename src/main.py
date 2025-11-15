import os
import shutil
from markdown import markdown_to_html_node, extract_title

def copy_static_to_public(src_dir="static", dest_dir="public"):
    """
    Recursively copy all contents from static directory to public directory.
    Deletes existing public directory first to ensure clean copy.
    """
    # Get absolute paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_path = os.path.join(base_dir, src_dir)
    dest_path = os.path.join(base_dir, dest_dir)
    
    # Delete destination directory if it exists
    if os.path.exists(dest_path):
        print(f"Deleting existing {dest_dir} directory...")
        shutil.rmtree(dest_path)
    
    # Create destination directory
    print(f"Creating {dest_dir} directory...")
    os.makedirs(dest_path)
    
    # Recursively copy contents
    _copy_directory_contents(src_path, dest_path)
    
    print(f"Successfully copied all contents from {src_dir} to {dest_dir}")

def _copy_directory_contents(src, dest):
    """
    Helper function to recursively copy directory contents.
    """
    if not os.path.exists(src):
        raise ValueError(f"Source directory {src} does not exist")
    
    # List all items in source directory
    items = os.listdir(src)
    
    for item in items:
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)
        
        if os.path.isfile(src_item):
            # Copy file
            print(f"Copying file: {src_item} -> {dest_item}")
            shutil.copy2(src_item, dest_item)
        elif os.path.isdir(src_item):
            # Create directory and recursively copy its contents
            print(f"Creating directory: {dest_item}")
            os.makedirs(dest_item, exist_ok=True)
            _copy_directory_contents(src_item, dest_item)

def generate_page(from_path, template_path, dest_path, base_dir=None):
    """
    Generate an HTML page from markdown content using a template.
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title
    title = extract_title(markdown_content)
    
    # Calculate relative path to root based on directory depth
    if base_dir:
        # Get relative path from dest to public root
        dest_dir = os.path.dirname(dest_path)
        rel_path = os.path.relpath(base_dir, dest_dir)
        if rel_path == '.':
            path_prefix = './'
        else:
            path_prefix = rel_path + '/'
    else:
        path_prefix = './'
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Fix absolute paths in content to be relative
    final_html = final_html.replace('href="/', f'href="{path_prefix}')
    final_html = final_html.replace('src="/', f'src="{path_prefix}')
    
    # Fix relative CSS path from template
    final_html = final_html.replace('href="./index.css"', f'href="{path_prefix}index.css"')
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write to destination file
    with open(dest_path, 'w') as f:
        f.write(final_html)
    
    print(f"Page generated successfully!")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path_root, public_root=None):
    """
    Recursively generate HTML pages from all markdown files in a directory.
    Maintains the directory structure in the destination.
    """
    # Track the public root directory for calculating relative paths
    if public_root is None:
        public_root = dest_dir_path_root
    
    # List all items in the content directory
    for item in os.listdir(dir_path_content):
        src_item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path_root, item)
        
        if os.path.isfile(src_item_path):
            # If it's a markdown file, generate HTML
            if item.endswith('.md'):
                # Replace .md with .html for destination
                dest_html_path = dest_item_path.replace('.md', '.html')
                # Pass the root public directory for path calculation
                generate_page(src_item_path, template_path, dest_html_path, base_dir=public_root)
        elif os.path.isdir(src_item_path):
            # If it's a directory, create corresponding directory and recurse
            os.makedirs(dest_item_path, exist_ok=True)
            generate_pages_recursive(src_item_path, template_path, dest_item_path, public_root)

def main():
    # Get base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Copy static files to public
    copy_static_to_public()
    
    # Generate all pages recursively from content directory
    generate_pages_recursive(
        os.path.join(base_dir, "content"),
        os.path.join(base_dir, "template.html"),
        os.path.join(base_dir, "public")
    )

if __name__ == "__main__":
    main()