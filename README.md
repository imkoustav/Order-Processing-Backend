# 🛒 Order Processing Backend

A scalable **Flask-based order processing system** using **PostgreSQL (Neon.tech)** and **Render** for deployment. It handles incoming orders asynchronously, processes them dynamically based on item count, and provides real-time metrics.

---

## **🚀 Live API Endpoint**
👉 **Base URL for metrics**: [https://order-processing-backend.onrender.com/metrics](https://order-processing-backend.onrender.com/metrics)

---

## **📌 Features**
- ✅ **Order Creation**: Accepts new orders with multiple items.
- ✅ **Order Processing**: Asynchronous status updates.
- ✅ **Metrics API**: Real-time order status tracking.
- ✅ **Queue System**: Ensures smooth processing.
- ✅ **Dynamic Processing Time**: Based on item count.

---

## **📤 API Endpoints & Usage**
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


### 2. Check Order Status
**Request**
curl -X GET https://order-processing-backend.onrender.com/orders/45

text
**Response**
{
"order_id": 45,
"status": "Processing"
}



### 3. Get Metrics
**Request**
curl -X GET https://order-processing-backend.onrender.com/metrics


**Response**
{
"total_orders": 50,
"pending_orders": 5,
"processing_orders": 3,
"completed_orders": 42,
"average_processing_time_seconds": "5.75"
}



## Setup & Installation
1. **Clone the Repo**
git clone https://github.com/imkoustav/Order-Processing-Backend.git
cd Order-Processing-Backend



2. **Create a Virtual Environment**
python -m venv venv
source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows



3. **Install Dependencies**
pip install -r requirements.txt



4. **Setup the Database**
Use Neon.tech as the PostgreSQL database (or a local database).
Create a `.env` file with:
DATABASE_URL=postgresql://your_username:your_password@your_neon_url/neondb?sslmode=require



5. **Run the Server**
python app.py



## Deployment on Render
1. **Connect GitHub**
Go to Render. Click New Web Service → Connect GitHub Repo.

2. **Set Up Environment Variables**
In Render Dashboard → Go to Environment Variables.
Add:
DATABASE_URL=postgresql://your_username:your_password@your_neon_url/neondb?sslmode=require



3. **Set Up Deployment**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

4. **Deploy & Monitor Logs**
Click Deploy and monitor Render Logs for any issues.

## Design Decisions & Trade-offs
- **Why Flask?**: Lightweight & easy to scale. Well-supported for REST APIs.
- **Queue-Based Processing**: Orders are added to a queue for background processing. Ensures scalability & better resource management.
- **PostgreSQL on Neon.tech**: Cloud-based & free-tier available. Eliminates need for local database setup.
- **Deployment on Render**: Free-tier hosting with continuous deployment. Auto-redeploy on GitHub push.

## Links
- **GitHub Repo**: Order Processing Backend
- **Deployed API**: https://order-processing-backend.onrender.com

## Future Improvements
- **Persistent queue (Redis)** instead of in-memory.
- **Better error handling & retries** for failed orders.
- **WebSocket** for real-time order updates.

## Assumptions
- Orders are processed FIFO (First-In-First-Out).
- Processing time is dynamic, based on the number of items:
- <3 items → 2s
- 3-10 items → 5s
- 10+ items → 10s
- Database failures are retried before marking as failed.

## Load Testing with Locust
1. **Install Locust**
pip install locust


2. **Run Locust**
- **For Local**:
  ```
  locust -f locustfile.py --host=http://127.0.0.1:5000
  ```
- **For Render**:
  ```
  locust -f locustfile.py --host=https://order-processing-backend.onrender.com
  ```
Open http://localhost:8089 in your browser to see the UI.

## Debugging & Common Issues
1. **Logs Not Updating?**
Restart service via Render Dashboard.
Run:
tail -f logs/app.log


2. **Orders Stuck in Pending?**
Check queue processing logs in Render.
