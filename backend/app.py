from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import json

# Add the current directory to Python path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from conflict_checker import ConflictChecker
from database import DatabaseManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the conflict checker and database
conflict_checker = ConflictChecker()
db = DatabaseManager()

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Prescription Conflict Checker API is running",
        "version": "1.0.0",
        "database": "SQLite connected"
    })

@app.route('/auth/signup', methods=['POST'])
def signup():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Validation
        if not name or not email or not password:
            return jsonify({"error": "Name, email, and password are required"}), 400
        
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        
        # Create user
        user = db.create_user(name, email, password)
        
        if not user:
            return jsonify({"error": "Failed to create user"}), 500
        
        return jsonify({
            "success": True,
            "message": "Account created successfully",
            "user": {
                "id": user['id'],
                "name": user['name'],
                "email": user['email']
            }
        })
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Error in signup: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Authenticate user
        user = db.authenticate_user(email, password)
        
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Create session
        session_id = db.create_session(user['id'])
        
        # Get user stats
        stats = db.get_user_stats(user['id'])
        
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user['id'],
                "name": user['name'],
                "email": user['email'],
                "last_login": user['last_login'],
                "stats": stats
            },
            "session_id": session_id
        })
        
    except Exception as e:
        print(f"Error in login: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    try:
        data = request.get_json()
        session_id = data.get('session_id') if data else None
        
        if session_id:
            db.invalidate_session(session_id)
        
        return jsonify({
            "success": True,
            "message": "Logout successful"
        })
        
    except Exception as e:
        print(f"Error in logout: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/auth/verify', methods=['POST'])
def verify_session():
    """Verify user session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id') if data else None
        
        if not session_id:
            return jsonify({"error": "Session ID required"}), 400
        
        user = db.get_session_user(session_id)
        
        if not user:
            return jsonify({"error": "Invalid or expired session"}), 401
        
        return jsonify({
            "success": True,
            "user": {
                "id": user['id'],
                "name": user['name'],
                "email": user['email']
            }
        })
        
    except Exception as e:
        print(f"Error in verify session: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/check-conflicts', methods=['POST'])
def check_conflicts():
    """
    Main endpoint to check for drug conflicts between two doctors' prescriptions
    Now includes user authentication and saves analysis history
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No JSON data provided"
            }), 400
        
        # Check for session authentication
        session_id = data.get('session_id')
        user = None
        
        if session_id:
            user = db.get_session_user(session_id)
            if not user:
                return jsonify({"error": "Invalid or expired session"}), 401
        
        # Extract medicine lists and user allergies
        doctor_a_medicines = data.get('doctorA_medicines', [])
        doctor_b_medicines = data.get('doctorB_medicines', [])
        user_allergies = data.get('user_allergies', [])
        
        # Validate input
        if not isinstance(doctor_a_medicines, list) or not isinstance(doctor_b_medicines, list):
            return jsonify({
                "error": "Medicine lists must be arrays"
            }), 400
            
        if not isinstance(user_allergies, list):
            return jsonify({
                "error": "User allergies must be an array"
            }), 400
        
        if len(doctor_a_medicines) == 0 and len(doctor_b_medicines) == 0:
            return jsonify({
                "error": "At least one medicine list must contain medicines"
            }), 400
        
        # Clean and normalize medicine names
        doctor_a_medicines = [medicine.lower().strip() for medicine in doctor_a_medicines if medicine.strip()]
        doctor_b_medicines = [medicine.lower().strip() for medicine in doctor_b_medicines if medicine.strip()]
        user_allergies = [allergy.strip() for allergy in user_allergies if allergy.strip()]
        
        print(f"Processing medicines - Doctor A: {doctor_a_medicines}, Doctor B: {doctor_b_medicines}, User Allergies: {user_allergies}")
        
        # Check for conflicts using the conflict checker
        result = conflict_checker.analyze_prescriptions(doctor_a_medicines, doctor_b_medicines, user_allergies)
        
        # Save analysis result to database if user is authenticated
        if user:
            interactions_count = len(result.get('interactions', []))
            risk_level = result.get('risk_level', 'LOW')
            
            db.save_analysis_result(
                user['id'], 
                doctor_a_medicines, 
                doctor_b_medicines, 
                interactions_count, 
                risk_level, 
                result
            )
            
            # Add user info to result
            result['user_analysis_saved'] = True
        
        print(f"Analysis result: {result}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in check_conflicts: {str(e)}")
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/analysis/history', methods=['POST'])
def get_analysis_history():
    """Get user's analysis history"""
    try:
        data = request.get_json()
        session_id = data.get('session_id') if data else None
        
        if not session_id:
            return jsonify({"error": "Session ID required"}), 400
        
        user = db.get_session_user(session_id)
        
        if not user:
            return jsonify({"error": "Invalid or expired session"}), 401
        
        limit = data.get('limit', 10)
        history = db.get_user_analysis_history(user['id'], limit)
        
        return jsonify({
            "success": True,
            "history": history,
            "user": {
                "name": user['name'],
                "email": user['email']
            }
        })
        
    except Exception as e:
        print(f"Error getting analysis history: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/medicines', methods=['GET'])
def get_known_medicines():
    """
    Get list of all medicines in the conflict database
    Useful for frontend validation and autocomplete
    """
    try:
        medicines = conflict_checker.get_all_known_medicines()
        return jsonify({
            "medicines": medicines,
            "count": len(medicines)
        })
    except Exception as e:
        return jsonify({
            "error": f"Error retrieving medicines: {str(e)}"
        }), 500

@app.route('/conflicts/<medicine>', methods=['GET'])
def get_medicine_conflicts(medicine):
    """
    Get conflicts for a specific medicine
    """
    try:
        medicine = medicine.lower().strip()
        conflicts = conflict_checker.get_medicine_conflicts(medicine)
        
        if conflicts is None:
            return jsonify({
                "error": f"Medicine '{medicine}' not found in database"
            }), 404
        
        return jsonify({
            "medicine": medicine,
            "conflicts": conflicts
        })
    except Exception as e:
        return jsonify({
            "error": f"Error retrieving conflicts: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested resource does not exist"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    print("Starting SPARD API...")
    print("🔧 Initializing SQLite database...")
    
    # Clean up expired sessions on startup
    db.cleanup_expired_sessions()
    
    print("Available endpoints:")
    print("  GET  /                    - Health check")
    print("  POST /auth/signup         - User registration")
    print("  POST /auth/login          - User login") 
    print("  POST /auth/logout         - User logout")
    print("  POST /auth/verify         - Verify session")
    print("  POST /check-conflicts     - Check for drug conflicts")
    print("  POST /analysis/history    - Get analysis history")
    print("  GET  /medicines           - Get all known medicines")
    print("  GET  /conflicts/<medicine> - Get conflicts for specific medicine")
    print()
    print("\n🔐 Database: SQLite with user authentication")
    print("📊 Create an account or login with existing credentials")
    print("Server will start on http://localhost:5000\n")
    print()
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )