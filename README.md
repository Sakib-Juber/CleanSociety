# 🌿 CleanSociety — Waste Management System

A society waste management portal where residents can report waste issues with live photos, and admins can track, resolve, and manage members.

---

## 📁 Project Structure

```
cleansociety/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── templates/
│   ├── base.html             # Base layout + navbar
│   ├── login.html            # Login page (with nature visuals)
│   ├── signup.html           # Registration page
│   ├── dashboard.html        # Resident dashboard + report form
│   ├── profile.html          # Resident profile edit page
│   ├── admin.html            # Admin – all reports
│   └── admin_users.html      # Admin – all society members
└── static/
    ├── css/style.css         # All styles (nature-green design system)
    ├── js/main.js            # Frontend JS (camera, previews, lightbox)
    └── uploads/              # Uploaded / captured photos
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
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

## ✨ Design Highlights

- **Nature-green theme** — deep forest greens, cream background, gold accents
- **Playfair Display** headings + **DM Sans** body for an elegant, clean feel
- **Animated leaf decorations** on auth pages (floating 🍃🌿🌱)
- **Stat cards** with subtle corner gradients
- **Lightbox** for viewing report photos in full size
- **Camera UI** — open, capture, retake, or upload from gallery
- **Responsive** — works on mobile and desktop

---

## ✨ Features

### Resident (User)
- Register with full name, email, mobile, profile photo, flat number
- Login securely
- Edit profile at any time
- Submit waste complaints with live camera capture or file upload
- View all personal reports and their status

### Admin
- See all complaints from all flats
- View all registered society members
- Remove a user (deletes reports + photos)
- Resolve or Delete individual reports
- Dashboard stats: total, pending, resolved, resolution rate
