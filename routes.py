from flask import Blueprint, request, jsonify, current_app
from models import db, Order, OrderSchema
from sqlalchemy.sql import func
# from queue_manager import order_queue
from queue_manager import add_order_to_queue
from datetime import datetime
from order_processor import start_order_processing

routes = Blueprint("routes", __name__)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
    
# @routes.route("/orders", methods=["POST"])
# def create_order():
#     try:
#         data = request.get_json()
#         new_order = Order(
#             user_id=data["user_id"],
#             item_ids=",".join(map(str, data["item_ids"])),
#             total_amount=data["total_amount"],
#             status="Pending"
#         )
#         db.session.add(new_order)
#         db.session.commit()
#         db.session.refresh(new_order)  # Ensures ID and properties are loaded

#         print(f"Adding order {new_order.id} to queue...")  # ✅ Debugging log

#         # ✅ Add the order to queue for processing
#         print(f"I am degugging this {new_order.id}")
#         add_order_to_queue(new_order.id)

#         print(f"Order created: {new_order.id}")
#         return order_schema.jsonify(new_order), 201
#     except Exception as e:
#         db.session.rollback()
#         print(f"Error creating order: {e}")
#         return jsonify({"error": "Failed to create order"}), 500 


@routes.route("/orders", methods=["POST"])
def create_order():
    try:
        data = request.get_json()
        new_order = Order(
            user_id=data["user_id"],
            item_ids=",".join(map(str, data["item_ids"])),
            total_amount=data["total_amount"],
            status="Pending"
        )
        db.session.add(new_order)
        db.session.commit()
        db.session.refresh(new_order)  # ✅ Ensure ID is available

        # print(f"Adding order {new_order.id} to queue...")  # ✅ Debugging log
        # add_order_to_queue(new_order.id)  # ✅ Add to queue

        print(f"🟢 Adding order {new_order.id} to queue...")
        add_order_to_queue(new_order.id)

        print(f"✅ Order {new_order.id} created successfully!")

        # ✅ Restart workers on new order
        start_order_processing(current_app) 
        
        return order_schema.jsonify(new_order), 201
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating order: {e}")
        return jsonify({"error": "Failed to create order"}), 500   


@routes.route("/orders/<int:order_id>", methods=["GET"])
def get_order_status(order_id):
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({"error": "Order not found"}), 404

    response = {
        "order_id": order.id,
        "status": order.status
    }

    # ✅ If order is "Completed", calculate time taken
    if order.status == "Completed" and order.created_at and order.completed_at:
        time_taken = (order.completed_at - order.created_at).total_seconds()
        response["time_taken_seconds"] = time_taken  # ✅ Add time taken to response

    return jsonify(response)


@routes.route("/metrics", methods=["GET"])
def get_metrics():
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status="Pending").count()
    processing_orders = Order.query.filter_by(status="Processing").count()
    completed_orders = Order.query.filter_by(status="Completed").count()

    # ✅ Calculate Average Processing Time (in seconds)
    avg_processing_time = db.session.query(
        func.avg(func.extract('epoch', Order.completed_at) - func.extract('epoch', Order.processing_at))
    ).filter(Order.completed_at.isnot(None)).scalar()

    return jsonify({
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "processing_orders": processing_orders,
        "completed_orders": completed_orders,
        "average_processing_time_seconds": avg_processing_time or 0  # ✅ Return 0 if no completed orders
    })
