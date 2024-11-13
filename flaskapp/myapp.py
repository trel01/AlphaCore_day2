from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS  # เพิ่มการนำเข้า CORS
import json
import threading
import websocket
from db_config import init_app
from models import save_machine_data

# สร้างแอป Flask
app = Flask(__name__)
CORS(app)  # เปิดใช้งาน CORS ให้กับทุกเส้นทาง
app.config['JWT_SECRET_KEY'] = 'admin'  # เปลี่ยนเป็นคีย์ที่ปลอดภัย
jwt = JWTManager(app)

# เชื่อมต่อ MongoDB
mongo = init_app(app)

# WebSocket URL
ws_url = "ws://technest.ddns.net:8001/ws"
key = "670a935a14221a12ae886117c99cacc7"

# ฟังก์ชันสำหรับการเชื่อมต่อกับ WebSocket และรับข้อมูล
def on_message(ws, message):
    # รับข้อมูลจาก WebSocket
    data = json.loads(message)
    print(f"Received data: {data}")
    
    # บันทึกข้อมูลลงใน MongoDB
    save_machine_data(mongo, data)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### WebSocket closed ###")

def on_open(ws):
    print("WebSocket opened")

def start_websocket():
    ws = websocket.WebSocketApp(ws_url, 
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

# เริ่ม WebSocket ในเธรดแยก
def start_websocket_thread():
    thread = threading.Thread(target=start_websocket)
    thread.daemon = True  # ให้เธรดนี้ทำงานในเบื้องหลัง
    thread.start()

# API สำหรับเข้าสู่ระบบและรับ JWT token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)  # แก้ไขให้ตรงกับชื่อฟิลด์
    password = request.json.get('password', None)  # แก้ไขให้ตรงกับชื่อฟิลด์
    
    # ตรวจสอบ username และ password
    if username != 'admin' or password != 'admin':  # เปลี่ยนเป็นค่า password ที่คุณต้องการ
        return jsonify({"msg": "Bad username or password"}), 401
    
    # สร้าง JWT token
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)
    
@app.route('/machine_data', methods=['GET'])
@jwt_required()
def get_machine_data():
    try:
        if not mongo.db:
            print("การเชื่อมต่อกับฐานข้อมูลล้มเหลว.")
            return jsonify({"error": "Database connection failed"}), 500

        collection = mongo.db.machine_data  # ตรวจสอบให้แน่ใจว่าคอลเล็กชันนี้มีอยู่
        if collection.count_documents({}) == 0:
            print("ไม่มีข้อมูลใน machine_data.")
            return jsonify({"error": "No machine data available"}), 404

        data = list(collection.find())
        return jsonify(data)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


# เริ่มต้นแอปพลิเคชัน Flask

if __name__ == '__main__':
    start_websocket_thread()  # เริ่ม WebSocket เมื่อแอปเริ่มทำงาน
    app.run(debug=True, host='0.0.0.0', port=5000)
