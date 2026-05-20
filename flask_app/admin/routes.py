from flask import Blueprint, render_template, request, redirect, url_for, session
from src.db import get_connection

admin = Blueprint("admin", __name__, template_folder="templates")

PASSWORD = "Aravindhan@2011"


# 🔒 AUTH CHECK (Reusable)
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


# 📊 DASHBOARD (WITH ANALYTICS)
@admin.route("/admin/dashboard")
def dashboard():
    if not is_admin():
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    conn.close()

    # 📊 Analytics
    high = sum(1 for p in patients if p[7] == "High")
    medium = sum(1 for p in patients if p[7] == "Medium")
    low = sum(1 for p in patients if p[7] == "Low")
    total = len(patients)

    return render_template(
        "dashboard.html",
        patients=patients,
        high=high,
        medium=medium,
        low=low,
        total=total
    )


# 🗑 DELETE
@admin.route("/admin/delete/<int:id>")
def delete_patient(id):
    if not is_admin():
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin.dashboard"))


# ✏️ EDIT PAGE
@admin.route("/admin/edit/<int:id>")
def edit_patient(id):
    if not is_admin():
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients WHERE id=%s", (id,))
    patient = cursor.fetchone()

    conn.close()

    return render_template("edit.html", patient=patient)


# 💾 UPDATE
@admin.route("/admin/update/<int:id>", methods=["POST"])
def update_patient(id):
    if not is_admin():
        return redirect(url_for("admin.login"))

    name = request.form["name"]
    age = request.form["age"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE patients SET name=%s, age=%s WHERE id=%s",
        (name, age, id)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin.dashboard"))