#! python3
import os
import re

BASE_URL = "https://bupt-os.github.io/website/"
# BASE_URL = "http://localhost:1313/"

def extract_title_from_markdown_header(markdown_content):
    """
    Extracts the title from a markdown file's header.

    Args:
    markdown_content (str): The content of the markdown file.

    Returns:
    str: The extracted title, or an empty string if no title is found.
    """
    # Regex pattern for extracting title
    title_pattern1 = r'^title:\s*"(.+)"$'
    title_pattern2 = r'^draft:\s*(.+)$'

    # Search for the pattern in the markdown content
    match1 = re.search(title_pattern1, markdown_content, re.MULTILINE)
    match2 = re.search(title_pattern2, markdown_content, re.MULTILINE)
    
    if match1 and match2:
        return match1.group(1), eval(match2.group(1).capitalize())
    else:
        return "",""
def list_markdown_files(directory):
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md") and not file.startswith("_"):
                relative_path = os.path.join(root, file)
                markdown_files.append(relative_path)
    return markdown_files

# Example usage
markdown_files = list_markdown_files("content\docs")
print(markdown_files)
for i in markdown_files:
    with open(i, "r", encoding="utf8") as f:
        content = f.read()
        title,draft = extract_title_from_markdown_header(content)
        if not draft:
            l = i.split("\\")[1:-1]
            l.append(title.strip().replace(" ", "-").lower())
            print("({})[{}]".format(title,BASE_URL + "/".join(l)))