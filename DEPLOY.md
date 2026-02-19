# Deploy Search Engine to Render

---

## Step 1: Create GitHub Account & Repository

1. Go to https://github.com and sign up
2. Click **"+"** (top right) → **"New repository"**
3. Name: `search-engine`
4. Select **Public**
5. Click **"Create repository"**

---

## Step 2: Install Git & Push Code

### Download Git
https://git-scm.com/downloads

### Push Code to GitHub

Open **PowerShell** in `C:\Users\Admin\Desktop\search-engine`:

```powershell
git init
git add .
git commit -m "Search Engine Project"
git remote add origin https://github.com/YOUR_USERNAME/search-engine.git
git branch -M main
git push -u origin main
```

> Replace `YOUR_USERNAME` with your GitHub username

---

## Step 3: Deploy on Render

1. Go to https://render.com → Sign up free
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub → Select `search-engine` repo

### Settings:

| Setting | Value |
|---------|-------|
| **Name** | `search-engine` |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn python_server.app:app` |
| **Instance Type** | `Free` |

4. Click **"Create Web Service"**
5. Wait 2-5 minutes

---

## Step 4: Done! 🎉

Your URL: `https://search-engine-xxxx.onrender.com`

Test searches: `python`, `machine learning`, `web development`

---

## Update App

```powershell
git add .
git commit -m "Update"
git push
```

Render auto-deploys!
