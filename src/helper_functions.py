# helper functions

import re
from textnode import *
from leafnode import LeafNode
from parentnode import ParentNode
from htmlnode import HTMLNode
from enum import Enum
import os
import shutil
    
def text_node_to_html_node(text_node):
    text_types = ["text", "bold", "italic", "code", "link", "image"]
    node_text_type = text_node.text_type

    if node_text_type not in text_types:
        raise Exception(f"Text nodes must be one of {text_types}")
    
    # Handle different text types
    if node_text_type == "text":
        return LeafNode(None, text_node.text)  # No tag, raw text
    if node_text_type == "bold":
        return LeafNode("b", text_node.text)  # <b> tag
    if node_text_type == "italic":
        return LeafNode("i", text_node.text)  # <i> tag
    if node_text_type == "code":
        return LeafNode("code", text_node.text)  # <code> tag
    if node_text_type == "link":
        if not text_node.url:  # Ensure url is provided for links
            raise Exception("Link nodes must have a URL.")
        return LeafNode("a", text_node.text, {"href": text_node.url})  # <a> tag with href
    if node_text_type == "image":
        if not text_node.url:  # Ensure src is provided for images
            raise Exception("Image nodes must have a URL.")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})  # <img> tag with src and alt
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Special case: If the node is completely empty, preserve it
        if node.text == "":
            new_nodes.append(TextNode("", node.text_type))
            continue
        
        # We only care about splitting "text" nodes
        if node.text_type == "text":
            # Split the text by the delimiter (e.g., backticks for code or * for italics)
            split_text = node.text.split(delimiter)
            
            # Alternately add text nodes with the original text_type and the new text_type
            for i, part in enumerate(split_text):
                if i % 2 == 0:
                    # Add normal text nodes for even indices (outside the delimiter) if part is not empty
                    if part:
                        new_nodes.append(TextNode(part, node.text_type))
                else:
                    # Add the special text nodes for odd indices (inside the delimiter)
                    new_nodes.append(TextNode(part, text_type))
        else:
            # If it's not a "text" node, just add it as is
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_link(old_nodes):
    """Splits text nodes by Markdown-style links using the extract_markdown_links function."""
    new_nodes = []

    for node in old_nodes:
        if node.text_type == "text":
            # Extract the links from the text
            links = extract_markdown_links(node.text)
            
            # Split the text based on the links
            split_text = re.split(r'(?<!!)\[(.*?)\]\((.*?)\)', node.text)

            # Iterate through the split text and insert links where appropriate
            link_index = 0
            for i, part in enumerate(split_text):
                if i % 3 == 0:
                    if part:
                        new_nodes.append(TextNode(part, "text"))
                elif i % 3 == 1:
                    link_text, link_url = links[link_index]
                    new_nodes.append(TextNode(link_text, "link", link_url))
                    link_index += 1
        else:
            # Non-text nodes are added unchanged
            new_nodes.append(node)

    return new_nodes


def split_nodes_image(old_nodes):
    """Splits text nodes by Markdown-style images using the extract_markdown_images function."""
    new_nodes = []

    for node in old_nodes:
        if node.text_type == "text":
            # Extract the images from the text
            images = extract_markdown_images(node.text)

            # Split the text based on the images
            split_text = re.split(r'!\[(.*?)\]\((.*?)\)', node.text)

            # Iterate through the split text and insert images where appropriate
            image_index = 0
            for i, part in enumerate(split_text):
                if i % 3 == 0:
                    if part:
                        new_nodes.append(TextNode(part, "text"))
                elif i % 3 == 1:
                    alt_text, image_url = images[image_index]
                    new_nodes.append(TextNode(alt_text, "image", image_url))
                    image_index += 1
        else:
            # Non-text nodes are added unchanged
            new_nodes.append(node)

    return new_nodes

def text_to_textnodes(text):
    """Converts raw text into a list of TextNode objects with appropriate types (text, link, image, etc.)."""

    nodes = [TextNode(text, "text")]
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def markdown_to_blocks(markdown):
    """Given a markdown string, will return a list of 'block' strings"""
    # Split the string into blocks
    split_blocks = markdown.split('\n\n')
    
    # Initialize the return list
    result_blocks = []
    
    # Loop over each block, removing leading and trailing whitespace and extra line breaks
    for block in split_blocks:
        stripped_block = block.strip()
        if stripped_block:
            result_blocks.append(stripped_block)
            
    return result_blocks

def block_to_block_type(block):
    """Inspects a single 'block' of markdown, returning a string representation of the block's 'type'"""
    # Headings (1-6 # characters followed by a space)
    if block.startswith("# "):
        return "heading-1"
    elif block.startswith("## "):
        return "heading-2"
    elif block.startswith("### "):
        return "heading-3"
    elif block.startswith("#### "):
        return "heading-4"
    elif block.startswith("##### "):
        return "heading-5"
    elif block.startswith("###### "):
        return "heading-6"

    # Code block (starts and ends with 3 backticks)
    if block.startswith("```") and block.endswith("```"):
        return "code"

    # Quote block (every line starts with a > character)
    if block and all(line.startswith(">") for line in block.splitlines()):
        return "quote"

    # Unordered list block (every line starts with * or - followed by a space)
    if block and all(line.startswith("* ") or line.startswith("- ") for line in block.splitlines()):
        return "unordered-list"

    # Ordered list block (every line starts with a number followed by . and a space)
    lines = block.splitlines()
    if block and all(line[:line.index(".")].isdigit() and line[line.index(".") + 1:].startswith(" ") for line in lines if "." in line):
        # Check if the numbers increment correctly
        numbers = [int(line[:line.index(".")]) for line in lines if "." in line]
        if numbers == list(range(1, len(numbers) + 1)):
            return "ordered-list"

    # If none of the above conditions are met, it's a paragraph
    return "paragraph"

def markdown_to_html_node(markdown):
    # Split the markdown into blocks
    markdown_blocks = markdown_to_blocks(markdown)
    
    # Define a dictionary mapping block types to HTML tags
    tags = {
        "heading-1":"h1",
        "heading-2":"h2",
        "heading-3":"h3",
        "heading-4":"h4",
        "heading-5":"h5",
        "heading-6":"h6",
        "code":"code",
        "quote":"blockquote",
        "unordered-list":"ul",
        "ordered-list":"ol",
        "paragraph":"p"
    }
    
    # Create a parent div HTMLNode to hold all the blocks
    parent_node = HTMLNode(tag="div", children=[])
    
    # Loop over each block
    for block in markdown_blocks:
        # Determine the type of block and HTML tag
        # print(f"Block: {block}")
        block_type = block_to_block_type(block)
        # print(f"Block Type: {block_type}")
        tag = tags.get(block_type, "p") # Default to paragraph
        
        if block_type.startswith('heading'):
            block = block.lstrip("#").strip()
        if block_type == "code":
            block = block.strip('```').strip()
        if block_type in ["unordered-list", "ordered-list"]:
            list_items = block.splitlines()
            block_node = HTMLNode(tag=tags[block_type], children=[
                HTMLNode(tag="li", children=text_to_children(item.strip("1234567890. *> -")))
                for item in list_items])
            
            parent_node.children.append(block_node)
            continue
        if block_type == "quote":
            block = block.lstrip(">").strip()  # Strip the `>` symbol and leading/trailing whitespace

        # Create an HTMLNode for this block
        block_node = HTMLNode(tag=tag, children=[])
        
        # Assign child HTMLNode objects to the block
        block_node.children = text_to_children(block)
        
        # Add this block node to the parent node's children
        parent_node.children.append(block_node)
        
    # Return the parent div node containing all the block nodes
    return parent_node

def text_to_children(text):
    # Use the text_to_textnodes function to break down the text into line elements
    text_nodes = text_to_textnodes(text)
    
    # Convert each TextNode into an HTMLNode
    children = []
    for text_node in text_nodes:
        
        children.append(text_node_to_html_node(text_node))
                  
    return children

def extract_title(markdown='') -> str:
    """Extracts the Title from a markdown document or raises an Exception if one isn't found."""
    # Check for the Title syntax in markdown
    has_title = markdown.startswith('# ')
    
    # Raise Exception if has_title is false
    if not has_title:
        raise ValueError("Document must have a header.")
    
    # Extract the title from the first line of the document
    # and strip it of trailing white-space.
    title = markdown.splitlines()[0].lstrip("# ").strip()
    
    # Check that we didn't get just a blank # for the title
    if not title:
        raise ValueError("Document must have non-empty title.")
    # Debug line
    # print(f"Title: {title}")
    # return the Title, if it was found.
    return title

def delete_destination_contents(dest_dir):
    """Deletes all contents of the destination directory."""
    # Check if the directory exists
    if os.path.exists(dest_dir):
        # Walk through the destination directory and remove everything inside it
        for root, dirs, files in os.walk(dest_dir):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                shutil.rmtree(dir_path)
                print(f"Deleted directory: {dir_path}")

def copy_directory_recursive(src_dir, dest_dir):
    """Recursively copies all files and directories from the source to the destination."""
    # If the destination directory doesn't exist, create it
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Traverse the source directory
    for root, dirs, files in os.walk(src_dir):
        # Compute the destination path for each directory
        dest_root = root.replace(src_dir, dest_dir, 1)
        
        # If the destination directory doesn't exist, create it
        if not os.path.exists(dest_root):
            os.makedirs(dest_root)
            print(f"Created directory: {dest_root}")
        
        # Copy all files in the current directory
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)
            shutil.copy2(src_file, dest_file)
            print(f"Copied file: {src_file} -> {dest_file}")
    
    print("Copying completed.")
    
def generate_page(from_path, template_path, dest_path):
    # Print status message
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file and Template
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    with open(template_path, 'r') as f:
        template_content = f.read()
        
    # Convert markdown to html using the markdown_to_html_node function
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title from the markdown using extract_title function
    title = extract_title(markdown_content)
    
    # Replace the placeholders in the template with the title and content
    final_html = template_content.replace('{{ Title }}', title)
    final_html = final_html.replace('{{ Content }}', html_content)
    
    # Ensure the destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    # Write the final HTML to the destination file
    with open(dest_path, 'w') as f:
        f.write(final_html)
        
    print(f"Page successfully generated at {dest_path}")
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """Crawl through content directory and generate HTML files from markdown using the same template."""
    
    # Crawl through the content directory
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                # Build the full path to the markdown file
                markdown_path = os.path.join(root, file)
                
                # Replace .md extension with .html and preserve the directory structure in dest_dir_path
                relative_path = os.path.relpath(markdown_path, dir_path_content)
                html_path = os.path.join(dest_dir_path, relative_path).replace(".md", ".html")
                
                # Ensure the destination directory exists
                dest_dir = os.path.dirname(html_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                # Generate the page using the existing generate_page function
                print(f"Generating HTML page for {markdown_path} -> {html_path}")
                generate_page(markdown_path, template_path, html_path)
                
