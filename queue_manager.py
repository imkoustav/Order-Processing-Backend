import queue

order_queue = queue.Queue()

def add_order_to_queue(order_id):
    """Adds an order to the processing queue"""
    print(f"Adding order {order_id} to queue")  # ✅ Debugging log
    order_queue.put(order_id)

