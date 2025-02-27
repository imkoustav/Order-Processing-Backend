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
```
curl -X POST https://order-processing-backend.onrender.com/orders \
     -H "Content-Type: application/json" \
     -d '{"user_id": 58, "item_ids": [101, 102, 103], "total_amount": 250.75}'
```

**Response**
```
HTTP/1.1 201 Created
Date: Thu, 27 Feb 2025 05:03:58 GMT
Content-Type: application/json
Transfer-Encoding: chunked
Connection: close
access-control-allow-origin: *
rndr-id: 1798be63-2964-48e0
vary: Accept-Encoding
x-render-origin-server: gunicorn
cf-cache-status: DYNAMIC
Server: cloudflare
CF-RAY: 9185a054ab094826-BOM
alt-svc: h3=":443"; ma=86400

{
  "completed_at": null,
  "created_at": "2025-02-27T05:03:55.677177",
  "id": 189,
  "item_ids": "101,102,103",
  "processing_at": null,
  "status": "Pending",
  "total_amount": 250.75,
  "user_id": 58
}
```

### 2. Check Order Status(provide the id and not the user_id in the id in the URI)
**Request**
```
curl -X GET https://order-processing-backend.onrender.com/orders/58
```


**Response**
```
HTTP/1.1 200 OK
Date: Thu, 27 Feb 2025 05:06:34 GMT
Content-Type: application/json
Transfer-Encoding: chunked
Connection: close
access-control-allow-origin: *
rndr-id: d9abf3a4-0a0f-44c9
vary: Accept-Encoding
x-render-origin-server: gunicorn
cf-cache-status: DYNAMIC
Server: cloudflare
CF-RAY: 9185a56dde5529ea-BOM
Content-Encoding: gzip
alt-svc: h3=":443"; ma=86400

{
  "order_id": 58,
  "status": "Completed",
  "time_taken_seconds": 6.752444
}
```


### 3. Get Metrics
**Request**
```
curl -X GET https://order-processing-backend.onrender.com/metrics
```

**Response**
```
HTTP/1.1 200 OK
Date: Thu, 27 Feb 2025 05:09:04 GMT
Content-Type: application/json
Transfer-Encoding: chunked
Connection: close
access-control-allow-origin: *
rndr-id: f55b6345-8a48-48dc
vary: Accept-Encoding
x-render-origin-server: gunicorn
cf-cache-status: DYNAMIC
Server: cloudflare
CF-RAY: 9185a916cc093c64-BOM
Content-Encoding: gzip
alt-svc: h3=":443"; ma=86400

{
  "average_processing_time_seconds": "6.3691064731182796",
  "completed_orders": 186,
  "pending_orders": 0,
  "processing_orders": 0,
  "total_orders": 186
}
```


## Setup & Installation
1. **Clone the Repo**
```
git clone https://github.com/imkoustav/Order-Processing-Backend.git
cd Order-Processing-Backend
```


3. **Create a Virtual Environment**
```
python -m venv venv
source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows
```


4. **Install Dependencies**
```
pip install -r requirements.txt
```


5. **Setup the Database**
```
Use Neon.tech as the PostgreSQL database (or a local database).
Create a `.env` file with:
```
```
DATABASE_URL=postgresql://your_username:your_password@your_neon_url/neondb?sslmode=require
```


6. **Run the Server**
```   
python app.py
```


## Deployment on Render for public API endpoint 
1. **Connect GitHub**
Go to Render. Click New Web Service → Connect GitHub Repo.

2. **Set Up Environment Variables**
```   
In Render Dashboard → Go to Environment Variables.
Add:
DATABASE_URL=postgresql://your_username:your_password@your_neon_url/neondb?sslmode=require
```


4. **Set Up Deployment**
```
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
```

4. **Deploy & Monitor Logs**
Click Deploy and monitor Render Logs for any issues.

## Design Decisions & Trade-offs
- **Why Flask?**: Lightweight & easy to scale. Well-supported for REST APIs.
- **Queue-Based Processing**: Orders are added to a queue for background processing. Ensures scalability & better resource management.
- **PostgreSQL on Neon.tech**: Cloud-based & free-tier available. Eliminates need for local database setup.
- **Deployment on Render**: Free-tier hosting with continuous deployment. Auto-redeploy on GitHub push.

## Links
- **GitHub Repo**: [https://github.com/imkoustav/Order-Processing-Backend](https://github.com/imkoustav/Order-Processing-Backend)
- **Deployed API for metrics**: [https://order-processing-backend.onrender.com/metrics](https://order-processing-backend.onrender.com/metrics)

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
```
pip install locust
```


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
```
tail -f logs/app.log
```

3. **Orders Stuck in Pending?**
Check queue processing logs in Render.
