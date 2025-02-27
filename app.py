import os
from dotenv import load_dotenv

load_dotenv()
print("🔍 DATABASE_URL from .env:", os.getenv("DATABASE_URL"))  # ✅ Debugging line

from flask import Flask
from flask_cors import CORS  # ✅ Import CORS
from config import Config
from models import db, ma
from routes import routes
from flask_migrate import Migrate
from order_processor import start_order_processing, stop_order_processing  # Import stop function
import signal
import sys
import threading
import time


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# print("🔍 Database URL:", app.config["SQLALCHEMY_DATABASE_URI"])
print("🔍 Database URL from Config:", app.config["SQLALCHEMY_DATABASE_URI"])  # ✅ Debugging line


db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)  # ✅ Initialize Flask-Migrate
app.register_blueprint(routes)

with app.app_context():
    db.create_all()  # Ensure tables are created
    start_order_processing(app)
    print("🚀 Order processing workers started!")  # ✅ Debugging log



# def monitor_workers():
#     while True:
#         active_threads = threading.active_count() - 1  
#         print(f"🔍 Checking workers... Active: {active_threads}")

#         if active_threads < 2:  
#             print("⚠️ No active workers found! Restarting workers...")
#             start_order_processing(app)

#         time.sleep(10)  # ✅ Check every 10 seconds

# threading.Thread(target=monitor_workers, daemon=True).start()
    

# Handle shutdown gracefully
def shutdown_handler(signal_received, frame):
    print("Shutting down gracefully...")
    stop_order_processing()  # Stop order processing thread
    sys.exit(0)

# Catch termination signals
signal.signal(signal.SIGINT, shutdown_handler)  # Handle Ctrl+C
signal.signal(signal.SIGTERM, shutdown_handler)  # Handle process termination

if __name__ == "__main__":
    app.run(debug=False)
