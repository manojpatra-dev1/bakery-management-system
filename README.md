# Bakery Order Management System

## Problem Understanding

The local bakery was facing the following challenges:
- **Order Loss**: Customer orders were sometimes missed due to manual tracking
- **Inefficient Tracking**: Staff found it difficult to track which orders were pending vs completed
- **Customer Inquiries**: Customers frequently called to check their order status
- **Lack of Insights**: Owner had no clear view of daily sales and popular products
- **Operational Chaos**: Managing orders during busy hours became confusing and error-prone

## Solution

A web-based order management system that helps the bakery:
- Track all orders from creation to completion
- View real-time order status
- Manage products and inventory
- Generate daily sales reports
- Reduce manual work and customer phone calls

---

## Assumptions Made

1. **Authentication**: For MVP, basic admin login only (no customer accounts yet)
2. **Payment**: Orders are assumed to be paid in-store (no online payment)
3. **Inventory**: No automatic inventory deduction (manual tracking)
4. **Email**: Email notifications are optional (can be added later)
5. **Multi-location**: System assumes single bakery location
6. **Users**: Admin/Staff role without complex permission levels

---

## Features Implemented (MVP)

### 1. **Product Management**
   - Add, view, edit, delete products
   - Set product prices
   - Mark products as available/unavailable

### 2. **Order Management**
   - Create new orders with customer details
   - Add multiple items per order
   - Auto-calculate total price
   - Update order status (pending → ready → completed)
   - View all orders in real-time

### 3. **Dashboard**
   - View all orders at a glance
   - Filter orders by status (All, Pending, Ready, Completed)
   - See customer name, phone, total price
   - Quick action buttons (View, Update status)
   - Auto-refresh every 5 seconds

### 4. **Order Details**
   - View complete order information
   - See itemized order details
   - Update status from order details page
   - Track order creation time

---

## Database Design

### **Products Table**


id (Primary Key)
name (String)
description (Text)
price (Decimal)
is_available (Boolean)
created_at (DateTime)


### **Orders Table**

id (Primary Key)
customer_name (String)
customer_phone (String)
customer_email (String, Optional)
status (Choice: pending, ready, completed, cancelled)
total_price (Decimal)
notes (Text, Optional)
created_at (DateTime)
updated_at (DateTime)


### **OrderItems Table**

id (Primary Key)
order_id (Foreign Key → Orders)
product_id (Foreign Key → Products)
quantity (Integer)
price_at_time (Decimal)


---

## Technology Stack

**Backend**: Django + Django REST Framework  
**Database**: SQLite (development), MySQL (production ready)  
**Frontend**: HTML, CSS, Bootstrap 5, jQuery  
**Version Control**: Git/GitHub  

---

## Setup Instructions

### **1. Clone Repository**
```bash
git clone <your-repo-url>
cd bakery_management
```

### **2. Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install django djangorestframework python-decouple
```

### **4. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **5. Create Superuser**
```bash
python manage.py createsuperuser
# Enter: username, email, password
```

### **6. Start Server**
```bash
python manage.py runserver
```

### **7. Access Application**
- **Frontend**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/

---

## How to Use

### **Adding Products** (via Admin)
1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Click "Products" → "Add Product"
4. Fill in name, description, price
5. Save

### **Creating Orders**
1. Go to http://127.0.0.1:8000/ (Dashboard)
2. Click "+ New Order"
3. Enter customer name and phone
4. Click "Select Product" and add items
5. Enter quantity
6. Click "+ Add Item" for more products
7. Click "✅ Create Order"

### **Managing Orders**
1. View all orders on dashboard
2. Filter by status (Pending, Ready, Completed)
3. Click "View" to see order details
4. Click "Update" to change status
5. Status updates in real-time

---

## Future Improvements

1. **Customer Portal**: Customers can check their order status online
2. **SMS/Email Notifications**: Auto-notify customers when order is ready
3. **Inventory Management**: Track ingredients and auto-deduct from orders
4. **Analytics Dashboard**: Sales reports, popular products, peak hours
5. **Online Payment**: Accept payments through Razorpay/PayPal
6. **Multi-location**: Support multiple bakery branches
7. **Mobile App**: Native iOS/Android app
8. **Advanced Permissions**: Role-based access (owner, manager, staff)
9. **WhatsApp Integration**: Receive/send orders via WhatsApp API
10. **Delivery Tracking**: Track order delivery status

---

## API Endpoints

**GET** `/api/products/` - List all products  
**POST** `/api/products/` - Create product  
**GET** `/api/orders/` - List all orders  
**POST** `/api/orders/` - Create order  
**GET** `/api/orders/{id}/` - Get order details  
**POST** `/api/orders/{id}/update_status/` - Update order status  
**GET** `/api/orders/today_orders/` - Get today's orders  

---

## Project Structure





bakery_management/

├── bakery_project/

│   ├── settings.py

│   ├── urls.py

│   └── wsgi.py

├── orders/

│   ├── migrations/

│   ├── templates/orders/

│   │   ├── base.html

│   │   ├── index.html

│   │   ├── add_order.html

│   │   └── order_detail.html

│   ├── models.py

│   ├── views.py

│   ├── serializers.py

│   ├── urls.py

│   └── admin.py

├── manage.py

└── README.md







---

## Notes

- Default database is SQLite (db.sqlite3) - suitable for small bakeries
- All order times are stored in UTC
- Password reset requires email configuration
- CORS is not enabled (add if building separate frontend)
