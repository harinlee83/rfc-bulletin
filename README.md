# Redeemer Fellowship Church Bulletin

A Python script that helps automate and organize weekly bulletin preparation for **Redeemer Fellowship Church**, using data pulled from the [Planning Center API](https://developer.planning.center/docs/#/overview/).

## 📌 Features

- Fetch latest plan data from Planning Center
- Extract and format:
  - Team members + roles
  - Service item descriptions
  - Sermon notes and outlines
- Display a checklist for weekly bulletin updates

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rfc-bulletin.git
cd rfc-bulletin
```

### 2. Set up a Python virtual environment (recommended)
```
# Create the virtual environment
python -m venv env

# Activate it
source env/bin/activate
```

### 3. Install dependencies
We use `beautifulsoup4`, `python-dotenv`, and `requests`:

```bash
pip install -r requirements.txt
```

### 4. Set your environment variables
Create a `.env` file with your Planning Center Personal Account Token credentials. You can get these from the [Planning Center Developer Portal](https://api.planningcenteronline.com/oauth/applications):

```
PLANNING_CENTER_APP_ID=???
PLANNING_CENTER_SECRET=???

# Name titles mapping as JSON string (use your actual team members here)
NAME_TITLES_JSON={"Person A": "Role 1", "Person B": "Role 2", "Person C": "Role 3", "Person D": "Role 4"}
```

## 🛠️ Usage
Run the main script to fetch the lastest updated worship plan
```
python main.py
```