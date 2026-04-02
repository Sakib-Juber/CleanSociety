# 🌿 CleanSociety — Waste Management System

A society waste management portal where residents can report waste issues with live photos, and admins can track, resolve, and manage members.

---

## 📁 Project Structure

```
cleansociety/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── .gitignore
├── templates/
│   ├── base.html             # Base layout for user pages
│   ├── login.html            # Login page (society building visual)
│   ├── signup.html           # Registration page
│   ├── dashboard.html        # Resident dashboard + report form
│   ├── profile.html          # Resident profile edit page
│   ├── admin.html            # Admin – all reports + member count
│   └── admin_users.html      # Admin – all society members
└── static/
    └── uploads/              # Uploaded / captured photos
```

---

## 🚀 How to Run in VS Code

### 1. Open the folder in VS Code
```
File → Open Folder → select cleansociety/
```

### 2. Open Terminal in VS Code  (Ctrl + `)

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

---

## 🔑 Default Admin Login
| Field    | Value      |
|----------|------------|
| Username | `admin`    |
| Password | `admin123` |

> ⚠️ Change this in `app.py → create_admin()` before deploying.

---

## ✨ Changes in This Version

### 🎨 New Login Page Design
- Split layout: Society building illustration (left) + login form (right)
- Animated glowing lamp posts, starfield, floating particles
- Society stats row: 24/7, Fast, Safe
- Matching design language for signup page too

### 🐛 Admin Fix: Member Count
- Admin dashboard now shows a **4th stat card: 🏘️ Society Members**
- Displays count of all registered residents (non-admin users)
- Clicking "View all members →" goes to the members management page

---

## ✨ Features

### Resident (User)
- Register with full name, email, mobile, profile photo, flat number
- Login securely with beautiful society-themed UI
- Edit profile at any time
- Submit waste complaints with live camera capture or file upload
- View all personal reports and their status

### Admin
- See all complaints from all flats
- **NEW: View total society member count on dashboard**
- View all registered society members as cards
- Remove a user (deletes reports + photos)
- Resolve or Delete individual reports
- Dashboard stats: total, pending, resolved, **members**

## 🚀 Roadmap
- [ ] Replace generic emojis with custom SVG vector icons.