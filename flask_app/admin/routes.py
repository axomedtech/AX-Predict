from flask import Blueprint, render_template, request, redirect, url_for, session
from src.db import get_connection

admin = Blueprint("admin", __name__, template_folder="templates")

PASSWORD = "Aravindhan@2011"


# =========================
# 🔒 AUTH CHECK
# =========================
def is_admin():
    return session.get("admin")


# =========================
# 🔐 LOGIN
# =========================
@admin.route("/admin", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        if request.form["password"] == PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin.dashboard"))

        return "❌ Wrong Password"

    return render_template("login.html")


# =========================
# 🚪 LOGOUT
# =========================
@admin.route("/admin/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))


# =========================
# 📊 DASHBOARD (FIXED 100%)
# =========================
@admin.route("/admin/dashboard")
def dashboard():

    if not is_admin():
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    # ✔ ONLY TAKE NEEDED COLUMNS (PREVENT INDEX BUGS)
    cursor.execute("""
        SELECT id, name, age, risk_level
        FROM patients
        ORDER BY id DESC
    """)

    patients = cursor.fetchall()
    conn.close()

    # =========================
    # 🔥 SAFE ANALYTICS
    # =========================

    high = 0
    medium = 0
    low = 0

    for p in patients:

        risk = str(p[3]).strip().upper()   # ✔ FIXED INDEX (risk_level)

        if risk == "HIGH":
            high += 1
        elif risk == "MEDIUM":
            medium += 1
        else:
            low += 1

    total = len(patients)

    high_percent = round((high / total) * 100) if total > 0 else 0

    return render_template(
        "dashboard.html",
        patients=patients,
        high=high,
        medium=medium,
        low=low,
        total=total,
        high_percent=high_percent
    )


# =========================
# 🗑 DELETE PATIENT
# =========================
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


# =========================
# ✏️ EDIT PATIENT
# =========================
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


# =========================
# 💾 UPDATE PATIENT
# =========================
@admin.route("/admin/update/<int:id>", methods=["POST"])
def update_patient(id):

    if not is_admin():
        return redirect(url_for("admin.login"))

    name = request.form["name"]
    age = request.form["age"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patients
        SET name=%s, age=%s
        WHERE id=%s
    """, (name, age, id))

    conn.commit()
    conn.close()

    return redirect(url_for("admin.dashboard"))