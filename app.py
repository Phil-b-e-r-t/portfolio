from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from models.message import db, Message

app = Flask(__name__)
app.secret_key = "change_this_to_a_long_random_secret_key"
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():

    new_message = Message(
        name=request.form["name"],
        email=request.form["email"],
        subject=request.form["subject"],
        message=request.form["message"]
    )

    db.session.add(new_message)
    db.session.commit()

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

    if search:

        messages = Message.query.filter(

            (Message.name.contains(search)) |

            (Message.email.contains(search)) |

            (Message.subject.contains(search))

        ).order_by(

            Message.created_at.desc()

        ).all()

    else:

        messages = Message.query.order_by(

            Message.created_at.desc()

        ).all()

    return render_template(

        "admin.html",

        messages=messages,

        search=search

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

if __name__ == "__main__":
    app.run(debug=True)