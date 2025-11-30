# Task Manager

A Streamlit-based task management application with Sheety API integration.

## Setup

1. Clone this repository
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Create a `.env` file with your credentials:
```
   SHEETY_API=your_api_url_here
   AUTH_USER=your_username
   AUTH_PASS=your_password
```
4. Run the app:
```bash
   streamlit run task_manager.py
```

## Deployment to Streamlit Cloud

1. Push code to GitHub (without .env file!)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add secrets in the app settings:
   - SHEETY_API
   - AUTH_USER
   - AUTH_PASS
```

---

## ✅ **Checklist Before Pushing to GitHub**
```
☑️ Created .env file locally (with your secrets)
☑️ Created .gitignore file (includes .env)
☑️ Updated code to use environment variables
☑️ Created requirements.txt
☑️ Created README.md
☑️ Tested locally to make sure it still works
☑️ Run: git status (make sure .env is NOT listed!)
☑️ Run: git add .
☑️ Run: git commit -m "Add task manager with secure credentials"
☑️ Run: git push
