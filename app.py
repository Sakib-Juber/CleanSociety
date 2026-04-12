from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash,
    send_from_directory,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from functools import wraps
import os
import base64

app = Flask(__name__)
app.secret_key = "your-secret-key-change-in-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///waste_mgmt.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

db = SQLAlchemy(app)

# ──────────────────────────────────────────
# MODELS
# ──────────────────────────────────────────


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    flat_number = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(10), default="user")
    full_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    mobile = db.Column(db.String(15), nullable=True)
    profile_photo = db.Column(db.String(200), nullable=True)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    reports = db.relationship("Report", backref="user", lazy=True)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    waste_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo_filename = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), default="Pending")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# ──────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_base64_image(data_url, prefix, user_id):
    if data_url and data_url.startswith("data:image"):
        _, encoded = data_url.split(",", 1)
        fname = f"{prefix}_{user_id}_{int(datetime.utcnow().timestamp())}.jpg"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
        with open(save_path, "wb") as fh:
            fh.write(base64.b64decode(encoded))
        return fname
    return None


# ──────────────────────────────────────────
# DECORATORS
# ──────────────────────────────────────────


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        if session.get("role") != "admin":
            flash("Access denied. Admins only.", "danger")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)

    return decorated


# ──────────────────────────────────────────
# AUTH ROUTES
# ──────────────────────────────────────────


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        flat_number = request.form["flat_number"].strip()
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip() or None
        mobile = request.form.get("mobile", "").strip() or None

        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose another.", "danger")
            return redirect(url_for("signup"))

        if email and User.query.filter_by(email=email).first():
            flash("Email already registered. Please use another.", "danger")
            return redirect(url_for("signup"))

        new_user = User(
            username=username,
            password=generate_password_hash(password),
            flat_number=flat_number,
            full_name=full_name,
            email=email,
            mobile=mobile,
        )

        profile_file = request.files.get("profile_photo")
        if (
            profile_file
            and profile_file.filename != ""
            and allowed_file(profile_file.filename)
        ):
            fname = secure_filename(
                f"profile_{username}_{int(datetime.utcnow().timestamp())}_{profile_file.filename}"
            )
            profile_file.save(os.path.join(app.config["UPLOAD_FOLDER"], fname))
            new_user.profile_photo = fname

        db.session.add(new_user)
        db.session.commit()
        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["flat_number"] = user.flat_number
            session["role"] = user.role
            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


# ──────────────────────────────────────────
# USER ROUTES
# ──────────────────────────────────────────


@app.route("/chat")
@login_required
def chat():
    # This looks for 'chat.html' inside your 'templates' folder
    return render_template("chat.html")


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    user = User.query.get(session["user_id"])

    if request.method == "POST":
        location = request.form["location"]
        waste_type = request.form["waste_type"].strip()
        description = request.form["description"].strip()
        photo_filename = None

        camera_data = request.form.get("camera_photo")
        photo_filename = save_base64_image(camera_data, "cam", user.id)

        if not photo_filename and "photo" in request.files:
            file = request.files["photo"]
            if file and file.filename != "" and allowed_file(file.filename):
                fname = secure_filename(
                    f"{user.id}_{int(datetime.utcnow().timestamp())}_{file.filename}"
                )
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], fname))
                photo_filename = fname

        report = Report(
            user_id=user.id,
            location=location,
            waste_type=waste_type,
            description=description,
            photo_filename=photo_filename,
        )
        db.session.add(report)
        db.session.commit()
        flash("Report submitted successfully!", "success")
        return redirect(url_for("dashboard"))

    reports = (
        Report.query.filter_by(user_id=user.id).order_by(Report.timestamp.desc()).all()
    )
    return render_template("dashboard.html", user=user, reports=reports)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = User.query.get(session["user_id"])

    if request.method == "POST":
        user.full_name = request.form.get("full_name", "").strip()
        user.mobile = request.form.get("mobile", "").strip() or None
        new_email = request.form.get("email", "").strip() or None

        if new_email and new_email != user.email:
            existing = User.query.filter_by(email=new_email).first()
            if existing and existing.id != user.id:
                flash("Email already in use.", "danger")
                return redirect(url_for("profile"))
        user.email = new_email

        profile_file = request.files.get("profile_photo")
        if (
            profile_file
            and profile_file.filename != ""
            and allowed_file(profile_file.filename)
        ):
            fname = secure_filename(
                f"profile_{user.username}_{int(datetime.utcnow().timestamp())}_{profile_file.filename}"
            )
            profile_file.save(os.path.join(app.config["UPLOAD_FOLDER"], fname))
            user.profile_photo = fname

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html", user=user)


# ──────────────────────────────────────────
# ADMIN ROUTES
# ──────────────────────────────────────────


@app.route("/admin")
@admin_required
def admin_dashboard():
    reports = Report.query.order_by(Report.timestamp.desc()).all()
    total = len(reports)
    pending = sum(1 for r in reports if r.status == "Pending")
    resolved = total - pending
    # ✅ FIX: Count all non-admin users (society members)
    members = User.query.filter_by(role="user").count()
    return render_template(
        "admin.html",
        reports=reports,
        total=total,
        pending=pending,
        resolved=resolved,
        members=members,
    )


@app.route("/admin/users")
@admin_required
def admin_users():
    users = User.query.filter_by(role="user").order_by(User.joined_at.desc()).all()
    return render_template("admin_users.html", users=users)


@app.route("/admin/users/delete/<int:user_id>")
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == "admin":
        flash("Cannot delete an admin account.", "danger")
        return redirect(url_for("admin_users"))

    for report in user.reports:
        if report.photo_filename:
            try:
                os.remove(
                    os.path.join(app.config["UPLOAD_FOLDER"], report.photo_filename)
                )
            except Exception:
                pass
        db.session.delete(report)

    if user.profile_photo:
        try:
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], user.profile_photo))
        except Exception:
            pass

    db.session.delete(user)
    db.session.commit()
    flash(f'User "{user.username}" and all their reports have been removed.', "warning")
    return redirect(url_for("admin_users"))


@app.route("/admin/resolve/<int:report_id>")
@admin_required
def resolve_report(report_id):
    report = Report.query.get_or_404(report_id)
    report.status = "Resolved"
    db.session.commit()
    flash(f"Report #{report_id} marked as Resolved.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/delete/<int:report_id>")
@admin_required
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    if report.photo_filename:
        try:
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], report.photo_filename))
        except Exception:
            pass
    db.session.delete(report)
    db.session.commit()
    flash(f"Report #{report_id} deleted.", "warning")
    return redirect(url_for("admin_dashboard"))


# ──────────────────────────────────────────
# INIT
# ──────────────────────────────────────────


def create_admin():
    if not User.query.filter_by(role="admin").first():
        admin = User(
            username="admin",
            password=generate_password_hash("admin123"),
            flat_number="Office",
            role="admin",
            full_name="Society Admin",
            email="admin@cleansociety.com",
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin account created → username: admin | password: admin123")


if __name__ == "__main__":
    with app.app_context():
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        db.create_all()
        create_admin()
    app.run(debug=True, host="0.0.0.0")
