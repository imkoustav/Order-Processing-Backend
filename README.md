# Order Processing Backend
A scalable order processing system built using Flask, PostgreSQL, and Render. It efficiently handles incoming orders, processes them asynchronously, and provides real-time metrics.

## Live API Endpoint
- **Base URL**: https://order-processing-backend.onrender.com

## Features
- **Order Creation**: Accepts new orders with multiple items.
- **Order Processing**: Handles order status updates asynchronously.
- **Metrics API**: Provides real-time stats on order status and average processing time.
- **Queue Management**: Uses an in-memory queue for efficient processing.
- **Dynamic Processing Time**: Based on item count.

## API Endpoints & Usage
### 1. Create an Order
**Request**

curl -X POST https://order-processing-backend.onrender.com/orders
-H "Content-Type: application/json"
-d '{"user_id": 104, "item_ids":101102103, "total_amount": 250.75}'

**Response**

{
"order_id": 45,
"user_id": 104,
"item_ids": "101,102,103",
"total_amount": 250.75,
"status": "Pending"
}
