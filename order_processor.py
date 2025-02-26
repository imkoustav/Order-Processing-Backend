import os
import threading
import time
from datetime import datetime  # ✅ Import datetime to track timestamps
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask import current_app
from models import db, Order  # Import Order model
from queue_manager import order_queue
from config import Config
from queue import Empty  # ✅ Import Empty to catch queue timeout errors


# # ✅ Create a separate session factory for the background thread
# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# ✅ Use environment variable directly
DATABASE_URL = os.getenv("DATABASE_URL", Config.SQLALCHEMY_DATABASE_URI)

# ✅ Fix the database engine creation
engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))

stop_event = threading.Event()

# def process_orders():
#     while not stop_event.is_set():
#         try:
#             print(f"Queue size: {order_queue.qsize()}")  # ✅ Debugging log
#             order_id = order_queue.get(timeout=5)  
#             print(f"Fetched order {order_id} from queue")  # ✅ Debugging log
            
#             session = Session()  
#             order = session.query(Order).get(order_id)  
#             if not order:
#                 session.close()
#                 continue

#             # ✅ Count number of items
#             item_count = len(order.item_ids.split(","))  # Convert string to list and count

#             # ✅ Determine processing time based on item count
#             if item_count < 3:
#                 processing_time = 2
#             elif 3 <= item_count <= 10:
#                 processing_time = 5
#             else:  # More than 10 items
#                 processing_time = 10

#             # ✅ Update status to "Processing"
#             order.status = "Processing"
#             order.processing_at = datetime.utcnow()
#             session.commit()
#             print(f"Updated order {order_id} to Processing (Processing Time: {processing_time} sec)")

#             # ✅ Simulate processing time dynamically
#             time.sleep(processing_time)

#             # ✅ Update status to "Completed"
#             order.status = "Completed"
#             order.completed_at = datetime.utcnow()
#             session.commit()
#             print(f"Updated order {order_id} to Completed")

#             order_queue.task_done()
#             session.close()

#         except Empty:
#             print("No orders to process. Waiting...")
#             continue  

#         except Exception as e:
#             print(f"Error processing order: {e}")


# def process_orders(app):
#     with app.app_context():  # ✅ Add app context for DB access
#         while not stop_event.is_set():
#             try:
#                 print(f"Queue size: {order_queue.qsize()}")  # ✅ Debugging log
#                 order_id = order_queue.get(timeout=5)  
#                 print(f"Fetched order {order_id} from queue")  # ✅ Debugging log

#                 session = Session()
#                 order = session.query(Order).get(order_id)  
#                 if not order:
#                     session.close()
#                     continue

#                 # ✅ Count number of items
#                 item_count = len(order.item_ids.split(","))

#                 # ✅ Determine processing time dynamically
#                 if item_count < 3:
#                     processing_time = 2
#                 elif 3 <= item_count <= 10:
#                     processing_time = 5
#                 else:
#                     processing_time = 10

#                 # ✅ Update status to "Processing"
#                 order.status = "Processing"
#                 order.processing_at = datetime.utcnow()
#                 session.commit()
#                 print(f"Updated order {order_id} to Processing (Processing Time: {processing_time} sec)")

#                 # ✅ Simulate processing time dynamically
#                 time.sleep(processing_time)

#                 # ✅ Update status to "Completed"
#                 order.status = "Completed"
#                 order.completed_at = datetime.utcnow()
#                 session.commit()
#                 print(f"Updated order {order_id} to Completed")

#                 order_queue.task_done()
#                 session.close()

#             except Empty:
#                 print("No orders to process. Waiting...")
#                 continue  

#             except Exception as e:
#                 print(f"Error processing order: {e}")


def process_orders():
    while not stop_event.is_set():
        try:
            print(f"Queue size: {order_queue.qsize()}")  # ✅ Debugging log

            order_id = order_queue.get(timeout=5)  
            print(f"Fetched order {order_id} from queue")  # ✅ Debugging log

            session = Session()  
            order = session.query(Order).get(order_id)  
            if not order:
                print(f"⚠️ Order {order_id} not found in DB!")
                session.close()
                continue

            print(f"✅ Processing order {order_id}...")  # ✅ Debugging log
            order.status = "Processing"
            order.processing_at = datetime.utcnow()
            session.commit()

            time.sleep(5)  # Simulated processing

            order.status = "Completed"
            order.completed_at = datetime.utcnow()
            session.commit()
            print(f"✅ Completed order {order_id}!")

            order_queue.task_done()
            session.close()

        except Empty:
            print("No orders to process. Waiting...")
            continue  

        except Exception as e:
            print(f"❌ Error processing order: {e}")



def estimate_worker_count(app):
    """Determine the number of workers dynamically based on pending order complexity."""
    with app.app_context():  # ✅ Use app passed from app.py
        pending_orders = db.session.query(Order).filter(Order.status == "Pending").all()

        if not pending_orders:
            return 2  # Default minimum workers when no orders exist

        # Calculate the average item count in pending orders
        total_items = sum(len(order.item_ids.split(",")) for order in pending_orders)
        avg_item_count = total_items / len(pending_orders)

        # Determine number of workers based on avg item count
        if avg_item_count < 3:
            return 2  # Low load, fewer workers
        elif 3 <= avg_item_count <= 10:
            return 5  # Moderate load
        else:
            return 10  # Heavy load, more workers


# def start_order_processing():
#     num_workers = estimate_worker_count()  # ✅ Dynamically determine workers
#     print(f"Starting {num_workers} order processing threads...")

#     for _ in range(num_workers):
#         worker_thread = threading.Thread(target=process_orders, daemon=True)
#         worker_thread.start()

#     print(f"Started {num_workers} order processing threads!")

# def start_order_processing(app):
#     num_workers = estimate_worker_count(app)  # ✅ Pass `app` to function
#     print(f"Starting {num_workers} order processing threads...")

#     for _ in range(num_workers):
#         worker_thread = threading.Thread(target=process_orders, daemon=True)
#         worker_thread.start()

#     print(f"Started {num_workers} order processing threads!")


# def start_order_processing(app):
#     num_workers = estimate_worker_count(app)  
#     print(f"Starting {num_workers} order processing threads...")

#     for _ in range(num_workers):
#         worker_thread = threading.Thread(target=process_orders, args=(app,), daemon=True)
#         worker_thread.start()

#     print(f"Started {num_workers} order processing threads!")

def start_order_processing(app):
    with app.app_context():  # ✅ Ensure DB session works
        pending_orders = db.session.query(Order).filter(Order.status == "Pending").all()

        for order in pending_orders:
            print(f"Re-adding pending order {order.id} to queue...")  # ✅ Debugging log
            order_queue.put(order.id)  # ✅ Re-add to queue

    num_workers = estimate_worker_count(app)
    print(f"Starting {num_workers} order processing threads...")

    for _ in range(num_workers):
        worker_thread = threading.Thread(target=process_orders, daemon=True)
        worker_thread.start()

    print(f"Started {num_workers} order processing threads!")



def stop_order_processing():
    stop_event.set()
