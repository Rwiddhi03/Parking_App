from . import db
import pandas as pd
import os

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    availability = db.Column(db.Integer, nullable=False)


def load_parking_data():
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'parking_lots.csv')
    df = pd.read_csv(csv_path)
    db.session.query(ParkingLot).delete()
    for index , row in df.iterrows():
        lot = ParkingLot(
            id=row['ID'],
            address=row['Address'],
            availability=row['Availability']
        )
        db.session.add(lot)
    
    db.session.commit()
    print("Parking data loaded successfully.")
