from flask import Flask,render_template,request,redirect,url_for,flash
from models.users import db , User 
from models.parking_lot import load_parking_data , ParkingLot
from models.parking_spot import load_parking_spot_data , ParkingSpot
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import login_user,LoginManager,current_user,login_required,logout_user
from datetime import datetime




app = Flask(__name__)


app.config['SECRET_KEY'] = 'abc123xyz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    db.create_all()
    load_parking_data()
    load_parking_spot_data() 


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
def home():
    return render_template("home.html")



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or Email already exists.")
            return redirect("/signup")
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect("/dashboard") 
    return render_template("signup.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect("/dashboard")  
        else:
            flash("Invalid username or password", "danger")
            return redirect("/login")

    return render_template("login.html")



@app.route("/dashboard")
@login_required
def dashboard():
    search_term = request.args.get('search', '').strip()

    if search_term:
        parking_lots = ParkingLot.query.filter(
            ParkingLot.address.ilike(f"%{search_term}%")
        ).all()
    else:
        parking_lots = ParkingLot.query.all()

    return render_template('dashboard.html', user=current_user.username.capitalize(), parking_lots=parking_lots , search_term=search_term)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")  


@app.route("/history")
@login_required
def history():
    return render_template("parking_history.html" , user=current_user.username.capitalize())


@app.route('/book_spot/<int:lot_id>', methods=['GET', 'POST'])
@login_required
def book_spot(lot_id):
    if request.method == 'POST':
        vehicle_no = request.form.get('vehicle_no')

        if not vehicle_no:
            flash("Vehicle number must be provided.", "error")
            return redirect(url_for('book_spot', lot_id=lot_id))

        # 🔍 Filter only by the given lot_id
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, is_booked=False).first()
        if not spot:
            flash("Sorry, no spots available in this lot.", "error")
            return redirect(url_for('book_spot', lot_id=lot_id))

        user_id = current_user.username[0].upper() + str(spot.spot_id)

        spot.is_booked = True
        spot.user_id = user_id
        spot.vehicle_no = vehicle_no
        spot.booked_at = datetime.now()

        lot = ParkingLot.query.filter_by(id=lot_id).first()
        if lot:
            lot.availability = lot.availability - 1

        db.session.commit()

        return redirect(url_for('dashboard', message="Spot booked successfully!")) 

    # GET request - preview the next free spot in this lot
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, is_booked=False).first()
    if not spot:
        return "No parking spots available in this lot."
    spot_id = spot.spot_id
    user_id = current_user.username[0].upper() + str(spot.spot_id)

    return render_template('book_spot.html', spot_id=spot_id, user_id = user_id , lot_id=lot_id)







if __name__ == '__main__':
    app.run(debug=True)