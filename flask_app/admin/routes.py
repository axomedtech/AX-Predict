from flask import Blueprint, render_template, request, redirect, url_for, session

admin = Blueprint("admin", __name__, template_folder="templates")

PASSWORD = "Aravindhan@2011"

# 🔒 AUTH CHECK
def is_admin():
    return session.get("admin")

# 🔐 LOGIN
@admin.route("/admin", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin.dashboard"))
        return "❌ Wrong Password"

    return render_template("login.html")

# 🚪 LOGOUT
@admin.route("/admin/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))

# 📊 DASHBOARD
@admin.route("/admin/dashboard")
def dashboard():
    if not is_admin():
        return redirect(url_for("admin.login"))

    patients = []

    return render_template(
        "dashboard.html",
        patients=patients,
        high=0,
        medium=0,
        low=0,
        total=0
    )