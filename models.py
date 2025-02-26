from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

db = SQLAlchemy()
ma = Marshmallow()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    item_ids = db.Column(db.String, nullable=False)  # Storing as a comma-separated string
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, default="Pending")  # Pending, Processing, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # ✅ Order created timestamp
    processing_at = db.Column(db.DateTime, nullable=True)  # ✅ When order moves to Processing
    completed_at = db.Column(db.DateTime, nullable=True)  # ✅ When order moves to Completed

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = True
