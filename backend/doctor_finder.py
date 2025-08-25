from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_cors import CORS
from datetime import datetime
import math
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'doctor-finder-enhanced-2024'
CORS(app)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['medical_app']
users = db['users']

# Complete dataset of 25 Indian doctors (5 for each specialization)
doctors_data = [
    # Tuberculosis Specialists
    {'id': 1, 'name': 'Dr. Arjun Mehta', 'age': 45, 'specialization': 'Tuberculosis', 'experience': 18, 'study': 'MBBS, MD Pulmonology AIIMS Delhi', 'rating': 4.8, 'city': 'Delhi', 'lat': 28.6139, 'lng': 77.2090, 'phone': '+91-9876543210'},
    {'id': 2, 'name': 'Dr. Priya Sharma', 'age': 38, 'specialization': 'Tuberculosis', 'experience': 12, 'study': 'MBBS, MD Respiratory Medicine KEM Mumbai', 'rating': 4.7, 'city': 'Mumbai', 'lat': 19.0760, 'lng': 72.8777, 'phone': '+91-9876543211'},
    {'id': 3, 'name': 'Dr. Rajesh Kumar', 'age': 42, 'specialization': 'Tuberculosis', 'experience': 15, 'study': 'MBBS, MD Chest Medicine CMC Vellore', 'rating': 4.6, 'city': 'Chennai', 'lat': 13.0827, 'lng': 80.2707, 'phone': '+91-9876543212'},
    {'id': 4, 'name': 'Dr. Sunita Reddy', 'age': 40, 'specialization': 'Tuberculosis', 'experience': 14, 'study': 'MBBS, MD Pulmonology NIMHANS Bengaluru', 'rating': 4.9, 'city': 'Bengaluru', 'lat': 12.9716, 'lng': 77.5946, 'phone': '+91-9876543213'},
    {'id': 5, 'name': 'Dr. Vikram Singh', 'age': 47, 'specialization': 'Tuberculosis', 'experience': 20, 'study': 'MBBS, MD Respiratory Medicine PGIMER Chandigarh', 'rating': 4.5, 'city': 'Hyderabad', 'lat': 17.3850, 'lng': 78.4867, 'phone': '+91-9876543214'},

    # Skin Cancer Specialists
    {'id': 6, 'name': 'Dr. Kavita Joshi', 'age': 43, 'specialization': 'Skin Cancer', 'experience': 16, 'study': 'MBBS, MD Dermatology AIIMS Delhi', 'rating': 4.8, 'city': 'Delhi', 'lat': 28.6139, 'lng': 77.2090, 'phone': '+91-9876543215'},
    {'id': 7, 'name': 'Dr. Rohit Agarwal', 'age': 39, 'specialization': 'Skin Cancer', 'experience': 13, 'study': 'MBBS, MD Dermatology Tata Memorial Mumbai', 'rating': 4.9, 'city': 'Mumbai', 'lat': 19.0760, 'lng': 72.8777, 'phone': '+91-9876543216'},
    {'id': 8, 'name': 'Dr. Meera Nair', 'age': 36, 'specialization': 'Skin Cancer', 'experience': 10, 'study': 'MBBS, MD Dermatology CMC Vellore', 'rating': 4.6, 'city': 'Kochi', 'lat': 9.9312, 'lng': 76.2673, 'phone': '+91-9876543217'},
    {'id': 9, 'name': 'Dr. Amit Patel', 'age': 44, 'specialization': 'Skin Cancer', 'experience': 17, 'study': 'MBBS, MD Oncology NIMHANS Bengaluru', 'rating': 4.7, 'city': 'Bengaluru', 'lat': 12.9716, 'lng': 77.5946, 'phone': '+91-9876543218'},
    {'id': 10, 'name': 'Dr. Neha Gupta', 'age': 41, 'specialization': 'Skin Cancer', 'experience': 15, 'study': 'MBBS, MD Dermatology NIMS Hyderabad', 'rating': 4.8, 'city': 'Hyderabad', 'lat': 17.3850, 'lng': 78.4867, 'phone': '+91-9876543219'},

    # Diabetic Retinopathy Specialists
    {'id': 11, 'name': 'Dr. Sanjay Chopra', 'age': 48, 'specialization': 'Diabetic Retinopathy', 'experience': 22, 'study': 'MBBS, MS Ophthalmology AIIMS Delhi', 'rating': 4.9, 'city': 'Delhi', 'lat': 28.6139, 'lng': 77.2090, 'phone': '+91-9876543220'},
    {'id': 12, 'name': 'Dr. Ritu Malhotra', 'age': 37, 'specialization': 'Diabetic Retinopathy', 'experience': 11, 'study': 'MBBS, MS Ophthalmology Sankara Nethralaya Chennai', 'rating': 4.7, 'city': 'Chennai', 'lat': 13.0827, 'lng': 80.2707, 'phone': '+91-9876543221'},
    {'id': 13, 'name': 'Dr. Deepak Rao', 'age': 45, 'specialization': 'Diabetic Retinopathy', 'experience': 19, 'study': 'MBBS, MS Ophthalmology LV Prasad Hyderabad', 'rating': 4.8, 'city': 'Hyderabad', 'lat': 17.3850, 'lng': 78.4867, 'phone': '+91-9876543222'},
    {'id': 14, 'name': 'Dr. Pooja Desai', 'age': 35, 'specialization': 'Diabetic Retinopathy', 'experience': 9, 'study': 'MBBS, MS Ophthalmology Narayana Nethralaya Bengaluru', 'rating': 4.6, 'city': 'Bengaluru', 'lat': 12.9716, 'lng': 77.5946, 'phone': '+91-9876543223'},
    {'id': 15, 'name': 'Dr. Ashish Verma', 'age': 42, 'specialization': 'Diabetic Retinopathy', 'experience': 16, 'study': 'MBBS, MS Ophthalmology KEM Mumbai', 'rating': 4.8, 'city': 'Mumbai', 'lat': 19.0760, 'lng': 72.8777, 'phone': '+91-9876543224'},

    # Alzheimer's Disease Specialists
    {'id': 16, 'name': 'Dr. Rekha Iyer', 'age': 50, 'specialization': 'Alzheimer\'s Disease', 'experience': 25, 'study': 'MBBS, DM Neurology AIIMS Delhi', 'rating': 4.9, 'city': 'Delhi', 'lat': 28.6139, 'lng': 77.2090, 'phone': '+91-9876543225'},
    {'id': 17, 'name': 'Dr. Manoj Tiwari', 'age': 46, 'specialization': 'Alzheimer\'s Disease', 'experience': 20, 'study': 'MBBS, DM Neurology SGPGIMS Lucknow', 'rating': 4.7, 'city': 'Lucknow', 'lat': 26.8467, 'lng': 80.9462, 'phone': '+91-9876543226'},
    {'id': 18, 'name': 'Dr. Shilpa Bhatt', 'age': 43, 'specialization': 'Alzheimer\'s Disease', 'experience': 17, 'study': 'MBBS, DM Neurology KEM Mumbai', 'rating': 4.8, 'city': 'Mumbai', 'lat': 19.0760, 'lng': 72.8777, 'phone': '+91-9876543227'},
    {'id': 19, 'name': 'Dr. Kiran Reddy', 'age': 41, 'specialization': 'Alzheimer\'s Disease', 'experience': 15, 'study': 'MBBS, DM Neurology NIMS Hyderabad', 'rating': 4.6, 'city': 'Hyderabad', 'lat': 17.3850, 'lng': 78.4867, 'phone': '+91-9876543228'},
    {'id': 20, 'name': 'Dr. Anand Pillai', 'age': 44, 'specialization': 'Alzheimer\'s Disease', 'experience': 18, 'study': 'MBBS, DM Neurology NIMHANS Bengaluru', 'rating': 4.8, 'city': 'Bengaluru', 'lat': 12.9716, 'lng': 77.5946, 'phone': '+91-9876543229'},

    # Bone Fracture Specialists
    {'id': 21, 'name': 'Dr. Suresh Jain', 'age': 49, 'specialization': 'Bone Fracture', 'experience': 23, 'study': 'MBBS, MS Orthopedics AIIMS Delhi', 'rating': 4.9, 'city': 'Delhi', 'lat': 28.6139, 'lng': 77.2090, 'phone': '+91-9876543230'},
    {'id': 22, 'name': 'Dr. Lakshmi Prasad', 'age': 38, 'specialization': 'Bone Fracture', 'experience': 12, 'study': 'MBBS, MS Orthopedics Manipal Hospital Bengaluru', 'rating': 4.7, 'city': 'Bengaluru', 'lat': 12.9716, 'lng': 77.5946, 'phone': '+91-9876543231'},
    {'id': 23, 'name': 'Dr. Ramesh Babu', 'age': 45, 'specialization': 'Bone Fracture', 'experience': 19, 'study': 'MBBS, MS Orthopedics CMC Vellore', 'rating': 4.8, 'city': 'Chennai', 'lat': 13.0827, 'lng': 80.2707, 'phone': '+91-9876543232'},
    {'id': 24, 'name': 'Dr. Arun Shetty', 'age': 40, 'specialization': 'Bone Fracture', 'experience': 14, 'study': 'MBBS, MS Orthopedics Kokilaben Mumbai', 'rating': 4.6, 'city': 'Mumbai', 'lat': 19.0760, 'lng': 72.8777, 'phone': '+91-9876543233'},
    {'id': 25, 'name': 'Dr. Priyanka Shah', 'age': 36, 'specialization': 'Bone Fracture', 'experience': 10, 'study': 'MBBS, MS Orthopedics Apollo Hospitals Hyderabad', 'rating': 4.7, 'city': 'Hyderabad', 'lat': 17.3850, 'lng': 78.4867, 'phone': '+91-9876543234'}
]

# Available time slots
time_slots = {
    'Morning': ['9:00 AM', '10:00 AM', '11:00 AM'],
    'Afternoon': ['2:00 PM', '3:00 PM', '4:00 PM'],
    'Evening': ['5:00 PM', '6:00 PM', '7:00 PM']
}

# Indian cities with coordinates
indian_cities = {
    'Delhi': {'lat': 28.6139, 'lng': 77.2090},
    'Mumbai': {'lat': 19.0760, 'lng': 72.8777},
    'Bengaluru': {'lat': 12.9716, 'lng': 77.5946},
    'Chennai': {'lat': 13.0827, 'lng': 80.2707},
    'Hyderabad': {'lat': 17.3850, 'lng': 78.4867},
    'Kolkata': {'lat': 22.5726, 'lng': 88.3639},
    'Pune': {'lat': 18.5204, 'lng': 73.8567},
    'Jaipur': {'lat': 26.9124, 'lng': 75.7873},
    'Ahmedabad': {'lat': 23.0225, 'lng': 72.5714},
    'Lucknow': {'lat': 26.8467, 'lng': 80.9462},
    'Kochi': {'lat': 9.9312, 'lng': 76.2673},
    'Coimbatore': {'lat': 11.0168, 'lng': 76.9558},
    'Madurai': {'lat': 9.9252, 'lng': 78.1198},
    'Gurgaon': {'lat': 28.4595, 'lng': 77.0266},
    'Noida': {'lat': 28.5355, 'lng': 77.3910}
}

patients = {}
bookings = []

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def get_doctor_by_id(doctor_id):
    for doctor in doctors_data:
        if doctor['id'] == doctor_id:
            return doctor
    return None

def filter_doctors_by_specialization_and_location(specialization, patient_city):
    specialized_doctors = [doc for doc in doctors_data if doc['specialization'] == specialization]
    patient_coords = indian_cities.get(patient_city, indian_cities['Delhi'])
    
    for doctor in specialized_doctors:
        distance = haversine_distance(
            patient_coords['lat'], patient_coords['lng'],
            doctor['lat'], doctor['lng']
        )
        doctor['distance'] = round(distance, 1)
        
        if doctor['city'].lower() == patient_city.lower():
            doctor['match_type'] = 'Same City'
        elif distance < 100:
            doctor['match_type'] = 'Nearby'
        else:
            doctor['match_type'] = 'Available'
    
    specialized_doctors.sort(key=lambda x: x['distance'])
    return specialized_doctors

@app.route('/api/auth/signup', methods=['POST'])
def api_signup():
    data = request.json
    
    if users.find_one({'email': data['email']}):
        return jsonify({'success': False, 'message': 'Email already exists'})
    
    if data['password'] != data['confirm_password']:
        return jsonify({'success': False, 'message': 'Passwords do not match'})
    
    user_data = {
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'password': generate_password_hash(data['password']),
        'role': data['role']
    }
    
    if data['role'] == 'doctor':
        user_data.update({
            'specialization': data['specialization'],
            'experience': data['experience'],
            'qualification': data['qualification']
        })
    else:
        user_data.update({
            'age': data['age'],
            'gender': data['gender'],
            'location': data['location']
        })
    
    users.insert_one(user_data)
    return jsonify({'success': True, 'message': 'Registration successful'})

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.json
    user = users.find_one({'email': data['email']})
    
    if not user:
        return jsonify({'success': False, 'message': 'Email not found'})
    elif user['role'] != data['role']:
        return jsonify({'success': False, 'message': 'Invalid role'})
    elif not check_password_hash(user['password'], data['password']):
        return jsonify({'success': False, 'message': 'Invalid password'})
    else:
        session['user_id'] = str(user['_id'])
        session['role'] = data['role']
        return jsonify({'success': True, 'user': {'name': user['name'], 'role': user['role']}})

@app.route('/api/doctors/search', methods=['POST'])
def api_search_doctors():
    data = request.json
    doctors = filter_doctors_by_specialization_and_location(data['specialization'], data['location'])
    return jsonify({'doctors': doctors})

@app.route('/api/booking/create', methods=['POST'])
def api_create_booking():
    data = request.json
    doctor = get_doctor_by_id(data['doctor_id'])
    
    booking = {
        'id': len(bookings) + 1,
        'doctor': doctor,
        'patient': data['patient'],
        'time_slot': data['time_slot'],
        'date': data['date'],
        'timestamp': datetime.now().isoformat()
    }
    
    bookings.append(booking)
    return jsonify({'success': True, 'booking': booking})

@app.route('/api/time-slots', methods=['GET'])
def api_get_time_slots():
    return jsonify({'time_slots': time_slots})

if __name__ == '__main__':
    app.run(debug=True, port=5001)