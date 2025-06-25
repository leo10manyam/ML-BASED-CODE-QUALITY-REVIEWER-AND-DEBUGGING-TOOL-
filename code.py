import os
import base64
import requests
import google.generativeai as genai
from fastapi import FastAPI
from urllib.parse import urlparse
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# GitHub API Configuration
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GitHub Token is missing!")

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class RepoLink(BaseModel):
    url: str
    path: str = ""

class FileRequest(BaseModel):
    owner: str
    repo: str
    file_path: str

# Helper: Extract owner/repo
def extract_owner_repo(url):
    path = urlparse(url).path.strip("/").split("/")
    if len(path) >= 2:
        return path[0], path[1]
    return None, None

# Endpoint: Get repo or folder files
@app.post("/get_files")
def get_repo_files(repo_link: RepoLink):
    owner, repo = extract_owner_repo(repo_link.url)
    if not owner or not repo:
        return {"error": "Invalid GitHub URL"}

    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{repo_link.path}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {"files": response.json(), "owner": owner, "repo": repo}
    return {"error": response.json()}

# Endpoint: Get file content
@app.post("/get_file_content")
def get_file_content(file_request: FileRequest):
    repo_info_url = f"{GITHUB_API_URL}/repos/{file_request.owner}/{file_request.repo}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    repo_info = requests.get(repo_info_url, headers=headers).json()

    default_branch = repo_info.get("default_branch", "main")
    url = f"{GITHUB_API_URL}/repos/{file_request.owner}/{file_request.repo}/contents/{file_request.file_path}?ref={default_branch}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_data = response.json()

        if isinstance(file_data, list):
            return {"type": "folder", "folder_contents": file_data}

        if "content" in file_data:
            content = base64.b64decode(file_data["content"]).decode("utf-8")
            return {"type": "file", "content": content}

        return {"error": "Unknown data format"}
    return {"error": response.json()}

# ✅ Endpoint: Review code with Gemini AI
@app.post("/review_code")
def review_code(file_request: FileRequest):
    file_content_response = get_file_content(file_request)

    if "error" in file_content_response:
        return file_content_response

    if file_content_response.get("type") != "file":
        return {"error": "Selected path is not a file."}

    content = file_content_response["content"]
    prompt = f"""You are a professional code reviewer. Review the following code and return your suggestions as a clear, numbered list. Each point should be concise and easy to understand. Use proper Markdown formatting. If code changes are suggested, include them inside python code blocks.

Code:
{content}
"""

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    # ✅ Return suggestions as a list of markdown strings (split by double newline)
    suggestions = response.text.strip().split("\n\n")

    return {
        "suggestions": suggestions
    }



######Frontend######
import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Code Review", layout="centered")

st.title("🤖 AI Code Review with Gemini")
repo_link = st.text_input("Enter GitHub Repo Link")

if st.button("Fetch Files"):
    with st.spinner("Fetching files..."):
        res = requests.post("http://127.0.0.1:8000/get_files", json={"url": repo_link})
        if res.ok:
            data = res.json()
            st.session_state['files'] = data['files']
            st.session_state['owner'] = data['owner']
            st.session_state['repo'] = data['repo']
            st.session_state['current_path'] = ""
            st.session_state['history'] = []  # Initialize navigation history
        else:
            st.error("Failed to fetch files.")

# Initialize session states
for key in ['files', 'owner', 'repo', 'current_path', 'selected_file', 'file_content', 'suggestions', 'history']:
    if key not in st.session_state:
        st.session_state[key] = None if key != 'history' else []

# Show Back button
if st.session_state['current_path']:
    if st.button("⬅ Back"):
        parent_path = os.path.dirname(st.session_state['current_path'])
        with st.spinner("Loading parent folder..."):
            res = requests.post("http://127.0.0.1:8000/get_files", json={"url": repo_link, "path": parent_path})
            if res.ok:
                data = res.json()
                st.session_state['files'] = data['files']
                st.session_state['current_path'] = parent_path
                if st.session_state['history']:
                    st.session_state['history'].pop()  # Move back in history

# Show files and folders
if st.session_state['files']:
    st.subheader("📂 Files and Folders")
    for f in st.session_state['files']:
        if st.button(f"{'📁' if f['type'] == 'dir' else '📄'} {f['name']}", key=f['path']):
            if f['type'] == 'dir':
                with st.spinner("Loading folder..."):
                    res = requests.post("http://127.0.0.1:8000/get_files", json={"url": repo_link, "path": f['path']})
                    if res.ok:
                        data = res.json()
                        # Save current path in history before navigating forward
                        st.session_state['history'].append(st.session_state['current_path'])
                        st.session_state['files'] = data['files']
                        st.session_state['current_path'] = f['path']
            else:
                with st.spinner("Loading file..."):
                    res = requests.post("http://127.0.0.1:8000/get_file_content", json={
                        "owner": st.session_state['owner'],
                        "repo": st.session_state['repo'],
                        "file_path": f['path']
                    })
                    if res.ok:
                        st.session_state['selected_file'] = f['path']
                        st.session_state['file_content'] = res.json()['content']
                        st.session_state['suggestions'] = None

# Show file content
if st.session_state['file_content']:
    st.subheader("📜 File Content")
    st.code(st.session_state['file_content'], language="python")

    if st.button("Model AI Suggestions"):
        with st.spinner("Reviewing code..."):
            res = requests.post("http://127.0.0.1:8000/review_code", json={
                "owner": st.session_state['owner'],
                "repo": st.session_state['repo'],
                "file_path": st.session_state['selected_file']
            })
            if res.ok:
                st.session_state['suggestions'] = res.json()['suggestions']
            else:
                st.error("Failed to review code.")

# Show suggestions
if st.session_state['suggestions']:
    st.subheader("💡Model AI Suggestions")
    for s in st.session_state['suggestions']:
        st.markdown(f"• {s}")
