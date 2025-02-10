import os
import datetime
import subprocess

# ✅ Blog directory
BLOG_DIR = "docs/blog/posts/"
os.makedirs(BLOG_DIR, exist_ok=True)

# ✅ Function to create a blog post
def get_blog_post():
    title = input("Enter the blog post title: ").strip()
    filename = title.lower().replace(" ", "-") + ".md"
    filepath = os.path.join(BLOG_DIR, filename).replace("\\", "/")  # Fix Windows paths

    # ✅ Ask for tags (comma-separated)
    tags_input = input("Enter tags (comma-separated, e.g., security, python, automation): ").strip()
    tags = ", ".join([tag.strip() for tag in tags_input.split(",") if tag.strip()])  # MkDocs Blog expects CSV tags

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

    # ✅ Properly formatted front matter (MkDocs Material Blog Plugin)
    markdown_content = f"""---
title: "{title}"
date: {datetime.date.today()}  # ✅ Ensures correct ISO format for MkDocs
tags: [{tags}]  # ✅ Ensures tags are properly formatted
description: ""
---

# {title}

{'\n'.join(content)}
"""

    # ✅ Save file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(markdown_content)

    print(f"\n✅ Blog post saved: {filepath}")
    return filename, filepath

# ✅ Function to commit & push
def push_to_git(filename):
    try:
        print("\n✅ Staging changes...")
        subprocess.run(["git", "add", "--all"], check=True)

        commit_message = f"📢 New Blog Post: {filename.replace('-', ' ').replace('.md', '').title()} | {datetime.date.today()}"
        print(f"📝 Committing with message: '{commit_message}'")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        print("\n🔄 Pulling latest changes from GitHub...")
        subprocess.run(["git", "pull", "origin", "main", "--rebase"], check=True)

        print("🚀 Pushing changes to GitHub...")
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print(f"✅ Successfully pushed '{filename}' to GitHub!")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Git operation failed: {e}")
        print("Manually resolve any conflicts and try again.")

# ✅ Run the script
if __name__ == "__main__":
    filename, filepath = get_blog_post()
    push_to_git(filename)
