import os
import datetime
import subprocess

# ✅ Define the blog post directory
BLOG_DIR = "docs/blog/posts/"
os.makedirs(BLOG_DIR, exist_ok=True)

def get_blog_post():
    title = input("Enter the blog post title: ").strip()
    filename = title.lower().replace(" ", "-") + ".md"
    filepath = os.path.join(BLOG_DIR, filename).replace("\\", "/")  # Windows-safe paths

    # ✅ Ensure proper YAML front matter syntax
    categories_input = input("Enter categories (comma-separated, e.g., security, python, automation): ").strip()
    categories = [cat.strip() for cat in categories_input.split(",") if cat.strip()]  # Convert to a list

    description = input("Enter a short description for the post: ").strip()

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

    # ✅ Corrected YAML metadata for MkDocs blog plugin
    markdown_content = f"""---
title: "{title}"
date: {datetime.date.today().isoformat()}
description: "{description}"
categories:
  - {("\n  - ").join(categories)}
---

# {title}

{'\n'.join(content)}
"""

    # ✅ Save the blog post
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(markdown_content)

    print(f"\n✅ Blog post saved: {filepath}")
    return filename, filepath

# ✅ Git commit & push function
def push_to_git(filename):
    try:
        print("\n✅ Checking for unstaged changes...")
        subprocess.run(["git", "add", "--all"], check=True)

        commit_message = f"📢 New Blog Post: {filename.replace('-', ' ').replace('.md', '').title()} | {datetime.date.today()}"
        print(f"📝 Committing with message: '{commit_message}'")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        print("\n🔄 Pulling latest changes from GitHub before pushing...")
        subprocess.run(["git", "pull", "--rebase"], check=True)

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
