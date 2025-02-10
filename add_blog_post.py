import os
import requests
import base64
import datetime


BLOG_DIR = "docs/blog/posts"
GITHUB_REPO = "zachariah-jones/wznt-blog"
BRANCH = "main"
GITHUB_TOKEN = os.getenv("GH_PAT_WIZNET")  # GitHub Token from Environment Variable

# ✅ Ensure the blog directory exists
os.makedirs(BLOG_DIR, exist_ok=True)

# ✅ Function to get user input
def get_blog_post():
    title = input("Enter the blog post title: ").strip()
    filename = title.lower().replace(" ", "-") + ".md"
    filepath = os.path.join(BLOG_DIR, filename)

    print("\nPaste your blog content below. Type EOF on a new line when done:\n")
    content = []
    while True:
        try:
            line = input()
            if line.strip().upper() == "EOF":
                break
            content.append(line)
        except KeyboardInterrupt:
            print("\n❌ Input interrupted. Exiting.")
            exit(1)

    # Convert to Markdown format with metadata
    markdown_content = f"""---
title: "{title}"
date: {datetime.date.today()}
tags: []
---

# {title}

{'\n'.join(content)}
"""

    # Save file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(markdown_content)

    print(f"\n✅ Blog post saved: {filepath}")
    return filename, filepath

# ✅ Function to commit & push to GitHub
def push_to_github(filename, filepath):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filepath}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Check if file exists in the repo
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()["sha"]  # File exists, so update
    else:
        sha = None  # File does not exist, create new

    with open(filepath, "rb") as file:
        content_b64 = base64.b64encode(file.read()).decode("utf-8")

    payload = {
        "message": f"Added/Updated blog post: {filename}",
        "content": content_b64,
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha  # Required for updates

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        print(f"✅ Successfully published {filename} to GitHub!")
    else:
        print(f"❌ Error publishing to GitHub: {response.json()}")

# ✅ Run the script
if __name__ == "__main__":
    filename, filepath = get_blog_post()
    push_to_github(filename, filepath)
