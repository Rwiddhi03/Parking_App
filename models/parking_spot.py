from . import db
from datetime import datetime
import pandas as pd
import os


class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, nullable=False)
    spot_id = db.Column(db.Integer, nullable=False)
    is_booked = db.Column(db.Boolean, nullable=False)  
    user_id = db.Column(db.String, nullable=True)
    vehicle_no = db.Column(db.String, nullable=True)
    booked_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

def load_parking_spot_data():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'parking_spots.csv')
    df = pd.read_csv(csv_path)
    db.session.query(ParkingSpot).delete()
    for index, row in df.iterrows():
        lot = ParkingSpot(
            lot_id=row['Lot ID'],
            spot_id=row['Spot ID'],
            is_booked=row['isBooked'],
            user_id=row['User ID'] if row['User ID'] != 'NA' else None,
            vehicle_no="000",  
            booked_at=None    
        )
        db.session.add(lot)
    
    db.session.commit()
    print("Parking spot data loaded successfully.")
