from datetime import datetime

# ฟังก์ชันบันทึกข้อมูล Machine ลง MongoDB
def save_machine_data(mongo, data):
    collection = mongo.db.machine_data  # ระบุ collection ที่จะบันทึกข้อมูล
    
    # บันทึกข้อมูลในรูปแบบที่สามารถจัดเก็บได้ง่ายใน MongoDB
    collection.insert_one({
        "Energy Consumption": data.get("Energy Consumption", {}),
        "Voltage": data.get("Voltage", {}),
        "Pressure": data.get("Pressure", None),
        "Force": data.get("Force", None),
        "Cycle Count": data.get("Cycle Count", None),
        "Position of the Punch": data.get("Position of the Punch", None),
        "timestamp": datetime.now()  # ใช้เวลาปัจจุบันในการบันทึก
    })
