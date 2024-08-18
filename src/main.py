import os
import shutil
from markdown_parse import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = ""
    out_text = ""
    with open(from_path, 'r') as md_f, open(template_path, 'r') as template_f:
        md = md_f.read()
        out_text = template_f.read()

    html_nodes = markdown_to_html_node(md)
    html_text = html_nodes.to_html()
    title = extract_title(md)

    out_text = out_text.replace("{{ Title }}", title)
    out_text = out_text.replace("{{ Content }}", html_text)

    directories = os.path.dirname(dest_path)
    os.makedirs(directories, exist_ok=True)
    print(dest_path)
    dest_path = dest_path.rsplit(".", 1)[0] + ".html"
    with open(dest_path, 'w') as out_f:
        out_f.write(out_text)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    src_list = os.listdir(dir_path_content)

    for item in src_list:
        src_file_path = os.path.join(dir_path_content, item)
        dst_file_path = os.path.join(dest_dir_path, item)
        
        if os.path.isfile(src_file_path) and item.rsplit('.', 1)[1] == "md":
            generate_page(src_file_path, template_path, dst_file_path)
        elif os.path.isdir(src_file_path):
            os.mkdir(dst_file_path)
            generate_pages_recursive(src_file_path, template_path, dst_file_path)
        else:
            err_message = f"Unsupported file type: {src_file_path}"
            raise Exception(err_message)

def recursive_file_copy(src_path, dst_path):
    src_list = os.listdir(src_path)

    for item in src_list:
        src_file_path = os.path.join(src_path, item)
        dst_file_path = os.path.join(dst_path, item)
        
        if os.path.isfile(src_file_path):
            print(f"Copying file... {item} to {dst_file_path}")
            shutil.copy(src_file_path, dst_file_path)
        elif os.path.isdir(src_file_path):
            os.mkdir(dst_file_path)
            recursive_file_copy(src_file_path, dst_file_path)
        else:
            err_message = f"Unsupported file type: {src_file_path}"
            raise Exception(err_message)

def main():
    #Accommodate for running script from src
    working_dir = os.getcwd()
    dir_name, curr_path = working_dir.rsplit('/', 1)
    print(dir_name, curr_path)
    print(working_dir)

    if curr_path == 'src':
        working_dir = dir_name

    #Ensure we're running script from either path with static or ../src
    print("This is the current path", working_dir)
    static_dir = os.path.join(working_dir, "static")
    if not os.path.exists(static_dir):
        raise Exception("Could not locate 'static' directory")
    
    #Ensure we're working with a clean public directory
    public_dir = os.path.join(working_dir, "public")
    if os.path.exists(public_dir):
        print(os.listdir(public_dir))
        shutil.rmtree(public_dir)
    os.mkdir(public_dir)
    
    recursive_file_copy(static_dir, public_dir)

    content_dir = os.path.join(working_dir, "content")
    content_list = os.listdir(content_dir)
    if not os.path.exists(content_dir):
        raise Exception("Could not locate 'content' directory")
    if "index.md" not in content_list:
        e_message = f"Could not find index.md at {content_dir}"
        raise Exception(e_message)
    
    template_path = os.path.join(working_dir, "template.html")
    generate_pages_recursive(content_dir, template_path, public_dir)

if __name__ == '__main__':
    main()
