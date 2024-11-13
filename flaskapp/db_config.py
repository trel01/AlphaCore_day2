from flask import Flask
from flask_pymongo import PyMongo
import os

def init_app(app):
    # ใช้ชื่อ container ของ MongoDB ที่ตั้งใน Docker Compose
    mongo_uri = os.getenv("MONGO_URI", "mongodb://admin:admin@my-mongodb2:27017")  # ใช้ environment variable สำหรับ Mongo URI
    app.config["MONGO_URI"] = mongo_uri
    
    # เริ่มต้นการเชื่อมต่อกับ MongoDB
    try:
        mongo = PyMongo(app)
        # ทดสอบการเชื่อมต่อกับ MongoDB
        mongo.db.command("ping")
        print("MongoDB connection successful!")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return None

    return mongo

if __name__ == "__main__":
    # สร้าง Flask app
    app = Flask(__name__)
    mongo = init_app(app)  # เก็บค่าที่ได้จากการเชื่อมต่อ MongoDB
    
    # ตรวจสอบว่าการเชื่อมต่อสำเร็จหรือไม่
    if mongo:
        print("Flask and MongoDB are connected successfully!")
    else:
        print("Failed to connect Flask with MongoDB.")
