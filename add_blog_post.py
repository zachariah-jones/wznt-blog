import os
import datetime
import subprocess

# ✅ Blog directory and GitHub repo details
BLOG_DIR = "docs/blog/posts/"
GITHUB_REPO = "zachariah-jones/wznt-blog"
BRANCH = "main"

# ✅ Ensure the blog directory exists
os.makedirs(BLOG_DIR, exist_ok=True)

# ✅ Function to get user input
def get_blog_post():
    title = input("Enter the blog post title: ").strip()
    filename = title.lower().replace(" ", "-") + ".md"
    filepath = os.path.join(BLOG_DIR, filename).replace("\\", "/")  # Fix Windows path issues

    # ✅ Ask user for tags (comma-separated)
    tags_input = input("Enter tags (comma-separated, e.g., cybersecurity, hacking, python): ").strip()
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]  # Fix YAML format

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

    # ✅ Fix: Ensure `date` is not in quotes (MkDocs requirement)
    markdown_content = f"""---
title: "{title}"
date: {datetime.date.today()}  # ✅ Proper date format (no quotes)
tags: {tags}
---

# {title}

{'\n'.join(content)}
"""

    # ✅ Save file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(markdown_content)

    print(f"\n✅ Blog post saved: {filepath}")
    return filename, filepath

# ✅ Function to commit & push to GitHub
def push_to_git(filename, filepath):
    try:
        print("\n✅ Staging ALL changes...")
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
    push_to_git(filename, filepath)
