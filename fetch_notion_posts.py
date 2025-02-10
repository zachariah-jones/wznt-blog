import os
import requests
import base64
from notion_client import Client
from markdownify import markdownify as md

# Load Notion API Key and Database ID from environment variables
NOTION_API_KEY = os.getenv("NOTION_TOKEN")
RAW_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")

# Ensure Database ID is cleaned (removes newlines, spaces, etc.)
DATABASE_ID = RAW_DATABASE_ID.replace("\n", "").replace(" ", "").strip()

# Debugging: Print database ID length
print(f"Database ID (sanitized): {DATABASE_ID}")
print(f"Database ID Length: {len(DATABASE_ID)}")

# Initialize Notion client
notion = Client(auth=NOTION_API_KEY)

# Fetch blog posts from Notion
def fetch_notion_posts():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"  # Latest stable version
    }

    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(f"❌ Error fetching Notion posts: {response.text}")
        return []

# Convert Notion content to Markdown
def notion_to_markdown(page):
    title = page["properties"]["Title"]["title"][0]["text"]["content"]
    content_blocks = page["properties"]["Content"]["rich_text"]
    content = "\n".join([md(block["text"]["content"]) for block in content_blocks])

    return title, content

# Push blog post to GitHub
def push_to_github(title, content):
    markdown_content = f"# {title}\n\n{content}"
    file_path = f"docs/posts/{title.replace(' ', '_')}.md"
    repo = "YOUR_GITHUB_USERNAME/YOUR_REPO"
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"

    content_b64 = base64.b64encode(markdown_content.encode()).decode()
    commit_message = f"Added new blog post: {title}"

    github_headers = {
        "Authorization": f"token {os.getenv('GH_PAT_WIZNET')}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {
        "message": commit_message,
        "content": content_b64,
        "branch": "main"
    }

    response = requests.put(url, headers=github_headers, json=payload)

    if response.status_code == 201:
        print(f"✅ Successfully published: {title}")
    else:
        print(f"❌ Error publishing to GitHub: {response.text}")

# Main execution
posts = fetch_notion_posts()
for post in posts:
    if post["properties"]["Status"]["select"]["name"] == "Published":
        title, content = notion_to_markdown(post)
        push_to_github(title, content)
