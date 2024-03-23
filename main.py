from flask import Flask,render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(300))
    password = db.Column(db.Integer)
    amount = db.Column(db.Integer)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        result = db.session.execute(db.select(User).where(User.email == email))
        # Note, email in db is unique so will only have one result.
        user = result.scalar()
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        new_user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=generate_password_hash(
                request.form["password"], method='pbkdf2:sha256', salt_length=8),
            amount=request.form["amount"])
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return render_template("deposit.html")
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u_email = request.form.get("email")
        u_pass = request.form.get("password")
        user = db.session.execute(db.select(User).where(User.email == u_email)).scalar()

        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, u_pass):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('op_page'))
    return render_template("login.html")


@app.route('/secrets')
@login_required
def op_page():
    return render_template("deposit.html")  # name=current_user.name,logged_in=True


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/deposit_successful', methods=["GET", "POST"])
def deposit():
    if request.method == "POST":
        u_id = current_user.get_id()
        u_pass = request.form.get("password")
        amt = request.form.get("amount")
        user = db.session.execute(db.select(User).where(User.id == u_id)).scalar()
        if not check_password_hash(user.password, u_pass):
            flash('Password incorrect, please try again.')
            return redirect(url_for('deposit'))
        else:
            user.amount = user.amount + int(amt)
            db.session.commit()
            return redirect(url_for("op_page    "))
    return render_template("Transaction.html",operation="deposit")

@app.route('/withdrawn_successful', methods=["GET", "POST"])
def withdraw():
    if request.method == "POST":
        u_id = current_user.get_id()
        u_pass = request.form.get("password")
        amt = request.form.get("amount")
        user = db.session.execute(db.select(User).where(User.id == u_id)).scalar()
        if not check_password_hash(user.password, u_pass):
            flash('Password incorrect, please try again.')
            return redirect(url_for('withdraw'))
        else:
            user.amount = user.amount - int(amt)
            db.session.commit()
            return redirect(url_for("op_page"))

    return render_template("Transaction.html",operation="withdraw")

@app.route("/balance",methods=["GET","POST"])
def balance():
    u_id = current_user.get_id()
    if request.method=="POST":
        logout_user()
        return redirect(url_for("home"))

    user = db.session.execute(db.select(User).where(User.id == u_id)).scalar()
    return render_template("Transaction.html", operation="balance",data=user)
if __name__ == "__main__":
    app.run(debug=True)
