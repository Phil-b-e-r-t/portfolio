from flask import Flask, render_template, request, redirect, url_for, session
from datetime import date
from config import Config
from models.message import db, Message
from models.admin import Admin
from flask_mail import Mail, Message as MailMessage

app = Flask(__name__)
mail = Mail()
app.secret_key = Config.SECRET_KEY
app.config.from_object(Config)

print("MAIL SERVER:", app.config.get("MAIL_SERVER"))
print("MAIL USER:", app.config.get("MAIL_USERNAME"))
print("MAIL PORT:", app.config.get("MAIL_PORT"))

db.init_app(app)
mail.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():

    name = request.form["name"]
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]

    # Save message to the database
    new_message = Message(
        name=name,
        email=email,
        subject=subject,
        message=message
    )

    db.session.add(new_message)
    db.session.commit()

    # -----------------------------
    # Email to YOU
    # -----------------------------
    admin_email = MailMessage(
        subject=f"New Portfolio Message: {subject}",
        recipients=["ampuriraphilbert@gmail.com"]
    )

    admin_email.body = f"""
You have received a new message from your portfolio.

Name: {name}

Email: {email}

Subject: {subject}

Message:

{message}
"""

    mail.send(admin_email)

    # -----------------------------
    # Auto Reply to Visitor
    # -----------------------------
    reply = MailMessage(
        subject="Thank you for contacting Ampurira Philbert",
        recipients=[email]
    )

    reply.body = f"""
Hello {name},

Thank you for contacting me through my portfolio.

I have successfully received your message.

I will review it and get back to you as soon as possible.

Best regards,

Ampurira Philbert
Software Engineer
Uganda Institute of Information and Communications Technology (UICT)
"""

    mail.send(reply)

    return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "12345":
            session["admin"] = True
            return redirect(url_for("admin"))

        return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect(url_for("login"))

    search = request.args.get("search")

    query = Message.query

    if search:
        query = query.filter(
            (Message.name.contains(search)) |
            (Message.email.contains(search)) |
            (Message.subject.contains(search))
        )

    messages = query.order_by(
        Message.created_at.desc()
    ).all()

    total_messages = Message.query.count()

    unread_messages = Message.query.filter_by(
        status="Unread"
    ).count()

    read_messages = Message.query.filter_by(
        status="Read"
    ).count()

    today_messages = Message.query.filter(
        db.func.date(Message.created_at) == date.today()
    ).count()

    return render_template(
        "admin.html",
        messages=messages,
        search=search,
        total_messages=total_messages,
        unread_messages=unread_messages,
        read_messages=read_messages,
        today_messages=today_messages
    )

@app.route("/message/<int:id>")
def view_message(id):

    if not session.get("admin"):
        return redirect(url_for("login"))

    message = Message.query.get_or_404(id)

    if message.status == "Unread":
        message.status = "Read"
        db.session.commit()

    return render_template(
        "view_message.html",
        message=message
    )

@app.route("/delete/<int:id>")
def delete_message(id):

    if not session.get("admin"):
        return redirect(url_for("login"))

    message = Message.query.get_or_404(id)

    db.session.delete(message)
    db.session.commit()

    return redirect(url_for("admin"))


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

print("\nRegistered Routes:")
for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == "__main__":
    app.run(debug=True)