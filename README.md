# 🏥 SPARD (Smart Prescription Analysis & Risk Detection)

**SPARD** is an advanced web application designed to prevent dangerous drug interactions by analyzing prescriptions from multiple doctors. Using cutting-edge OCR technology and a comprehensive medical database, SPARD provides real-time conflict detection, allergy management, and risk assessment to ensure patient safety.

## 🌟 Key Features

### 🔍 **Intelligent OCR Processing**
- Upload prescription images from multiple doctors
- Automatic medicine extraction using Tesseract.js OCR engine
- Real-time progress tracking with visual feedback
- Support for PNG, JPG, JPEG image formats

### 💊 **Comprehensive Conflict Analysis**
- **Drug-Drug Interactions**: Detection of dangerous medicine combinations
- **Allergy Conflicts**: User-specific allergy checking against prescribed medicines
- **Risk Assessment**: Categorized as HIGH, MEDIUM, or LOW severity levels
- **Medical Database**: 50+ medicines with detailed interaction profiles

### 👤 **User Management System**
- **Secure Authentication**: User registration and login with bcrypt encryption
- **Personal Allergy Profiles**: Manual allergy input with exact dataset matching
- **Session Management**: Secure user sessions with automatic expiration
- **Data Persistence**: User allergies and analysis history storage

### 🎨 **Modern User Interface**
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Medical Theme**: Professional healthcare-inspired design
- **Interactive Elements**: Drag-and-drop uploads, hover effects, smooth animations
- **Real-time Feedback**: Progress bars, loading states, and instant validation

### 🔒 **Security & Privacy**
- **Database Storage**: SQLite database for secure user data management
- **Password Security**: Bcrypt hashing with salt for password protection
- **Session Security**: UUID-based session tokens with expiration
- **Local Processing**: OCR processing done client-side for privacy

## 🚀 Technology Stack

### **Frontend**
- **HTML5/CSS3**: Modern semantic markup and advanced styling
- **JavaScript ES6+**: Modern JavaScript with async/await patterns
- **Tesseract.js**: Client-side OCR for prescription image processing
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox

### **Backend**
- **Python 3.8+**: Core backend language
- **Flask 2.3.3**: Lightweight web framework
- **SQLite**: Embedded database for user management
- **bcrypt 4.0.1**: Password hashing and authentication
- **Flask-CORS**: Cross-origin resource sharing support

## 📊 Medical Database

SPARD includes an extensive medical conflict database covering:
- **50+ Common Medications**: Comprehensive coverage of frequently prescribed drugs
- **Drug Interactions**: Detailed conflict descriptions and medical reasoning
- **Allergy Information**: Medicine-specific allergy contraindications
- **Risk Categorization**: Scientific severity classification system

## 🗂️ Project Architecture

```
spard/
├── frontend/
│   ├── index.html           # Main SPARD application interface
│   ├── login.html          # Authentication (login/signup) page
│   ├── style.css           # Modern responsive UI styling
│   ├── auth.css            # Authentication page styling
│   ├── script.js           # OCR processing & API integration
│   ├── auth.js             # Authentication logic
│   └── images/             # Background images and assets
├── backend/
│   ├── app.py              # Flask REST API server
│   ├── conflict_checker.py # Drug conflict analysis engine
│   ├── database.py         # SQLite database management
│   ├── requirements.txt    # Python dependencies
│   └── prescription_conflicts.db  # SQLite database file
└── README.md               # Project documentation
```

## 🚀 Installation & Setup

### **System Requirements**
- **Python 3.8+** (for Flask backend)
- **Modern Web Browser** (Chrome, Firefox, Safari, Edge)
- **Internet Connection** (for Tesseract.js CDN)
- **4GB RAM minimum** (for OCR processing)

### **1️⃣ Backend Setup**

```powershell
# Clone or download the SPARD project
cd prescription-conflict-checker/backend

# Install required Python packages
pip install -r requirements.txt

# Start the SPARD API server
python app.py
```

**Backend Server**: `http://localhost:5000`  
**Status**: Look for "Starting SPARD API..." message

### **2️⃣ Frontend Setup**

```powershell
# Navigate to frontend directory
cd ../frontend

# Start static file server
python -m http.server 8080

# Alternative servers:
# npx serve . (if Node.js installed)
# php -S localhost:8080 (if PHP installed)
```

**Frontend Access**: `http://localhost:8080`

### **3️⃣ First Time Usage**

1. **Create Account**: 
   - Open `http://localhost:8080/login.html`
   - Click "Create Account" and register
   - Complete the signup form

2. **Login**: 
   - Sign in with your credentials
   - You'll be redirected to the main SPARD interface

3. **Add Your Allergies**:
   - Enter known allergies in the allergy section
   - These will be checked against all prescriptions

4. **Upload Prescriptions**:
   - Upload images from Doctor A and Doctor B
   - Wait for OCR extraction to complete

5. **Analyze Conflicts**:
   - Click "Check for Conflicts"
   - Review detailed results and risk assessments

## 📱 How to Use SPARD

### **Step-by-Step Workflow**

#### **🔐 Authentication**
- **New Users**: Register with name, email, and secure password
- **Returning Users**: Login with existing credentials
- **Security**: All passwords encrypted with bcrypt hashing

#### **🚫 Allergy Management**
- Add personal allergies using the input field
- Allergies are matched against the medical database
- Remove allergies by clicking the 'x' button
- All allergies are saved to your user profile

#### **📄 Prescription Upload**
- **Drag & Drop**: Drag prescription images onto upload areas
- **Click Upload**: Click to browse and select images
- **Supported Formats**: PNG, JPG, JPEG files
- **OCR Processing**: Watch real-time progress bars

#### **🔍 Medicine Extraction**
- Tesseract.js automatically extracts text from images
- Medicine names are intelligently parsed and filtered
- Extracted medicines appear as colored tags
- Data is automatically saved to browser storage

#### **⚕️ Conflict Analysis**
- Click "Check for Conflicts" to analyze prescriptions
- System checks for:
  - **Drug-Drug Interactions**: Between Doctor A and B medicines
  - **Allergy Conflicts**: Your allergies vs prescribed medicines
  - **Risk Assessment**: HIGH/MEDIUM/LOW severity levels

#### **📊 Results Interpretation**
- **GREEN**: Low risk or no conflicts found
- **ORANGE**: Medium risk - caution advised
- **RED**: High risk - immediate medical consultation recommended
- **Detailed Explanations**: Medical reasoning for each conflict

## 🔧 Technical Implementation

### **🔍 OCR Processing Engine**

```javascript
// Tesseract.js OCR implementation
const processImage = async (file, doctorType) => {
    const { data: { text } } = await Tesseract.recognize(file, 'eng', {
        logger: progress => {
            updateProgressBar(doctorType, progress.progress * 100);
        }
    });
    
    // Extract and filter medicine names
    const medicines = extractMedicinesFromText(text);
    
    // Save to localStorage for persistence
    localStorage.setItem(doctorType, JSON.stringify(medicines));
    displayMedicines(medicines, doctorType);
};
```

### **🔐 User Authentication System**

```python
# Flask backend authentication
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    user = get_user_by_email(data['email'])
    
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        session_token = str(uuid.uuid4())
        create_user_session(user['id'], session_token)
        return jsonify({'success': True, 'token': session_token})
    
    return jsonify({'success': False, 'message': 'Invalid credentials'})
```

### **💊 Conflict Detection Algorithm**

```python
def find_conflicts(doctorA_medicines, doctorB_medicines, user_allergies):
    conflicts = []
    
    # Check drug-drug interactions
    for med_a in doctorA_medicines:
        for med_b in doctorB_medicines:
            if has_conflict(med_a, med_b):
                conflicts.append({
                    'type': 'drug_interaction',
                    'medicines': [med_a, med_b],
                    'severity': get_severity(med_a, med_b),
                    'reason': get_conflict_reason(med_a, med_b)
                })
    
    # Check allergy conflicts
    for allergy in user_allergies:
        for medicine in doctorA_medicines + doctorB_medicines:
            if has_allergy_conflict(allergy, medicine):
                conflicts.append({
                    'type': 'allergy_conflict',
                    'allergy': allergy,
                    'medicine': medicine,
                    'severity': 'HIGH',
                    'reason': f'Patient allergic to {allergy}, conflicts with {medicine}'
                })
    
    return conflicts
```

### **📊 Medical Database Structure**

```python
CONFLICTS_DATABASE = {
    "metformin": {
        "conflicts": [
            {
                "drug": "ibuprofen",
                "severity": "MEDIUM",
                "reason": "Ibuprofen can destabilize blood sugar levels when combined with Metformin"
            }
        ],
        "allergy_conflicts": ["sulfa", "metformin"]
    },
    
    "aspirin": {
        "conflicts": [
            {
                "drug": "warfarin",
                "severity": "HIGH", 
                "reason": "Increased risk of bleeding when combined"
            }
        ],
        "allergy_conflicts": ["aspirin", "salicylates"]
    }
}
```

## 🎯 Use Cases & Benefits

### **👨‍⚕️ For Healthcare Providers**
- **Multi-Doctor Coordination**: Identify conflicts when patients see multiple specialists
- **Emergency Situations**: Quick conflict checking in urgent care settings
- **Prescription Review**: Double-check medicine combinations before prescribing
- **Patient Safety**: Reduce adverse drug reactions and medical errors

### **🏥 For Medical Facilities**
- **Quality Assurance**: Implement systematic conflict checking protocols
- **Risk Management**: Reduce liability from preventable drug interactions
- **Efficiency**: Streamline prescription review processes
- **Documentation**: Track and analyze prescription conflict patterns

### **👤 For Patients**
- **Personal Safety**: Verify prescriptions before taking new medicines
- **Allergy Management**: Track personal allergies across different doctors
- **Family Care**: Check medicine conflicts for family members
- **Travel Medicine**: Verify international prescriptions for conflicts

## 🛡️ Security & Privacy Features

### **Data Protection**
- **Local OCR Processing**: Images processed on user's device, not uploaded to servers
- **Encrypted Storage**: User passwords hashed with bcrypt + salt
- **Session Security**: UUID-based tokens with automatic expiration
- **Database Security**: SQLite with parameterized queries to prevent SQL injection

### **Privacy Compliance**
- **Minimal Data Collection**: Only stores essential user information
- **No Image Storage**: Prescription images are not saved or transmitted
- **User Control**: Users can delete their accounts and data
- **Transparent Processing**: Clear indication of what data is processed and how

## 🔧 Troubleshooting

### **Common Issues**

**Backend Won't Start**
```powershell
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check port availability
netstat -an | findstr 5000
```

**OCR Not Working**
- Ensure stable internet connection (Tesseract.js loads from CDN)
- Try uploading clearer, higher resolution images
- Supported formats: PNG, JPG, JPEG only
- Check browser console for JavaScript errors

**Background Image Not Loading**
- Verify image file is in `frontend/images/` directory
- Clear browser cache (Ctrl+F5)
- Check file permissions and format

**Authentication Issues**
- Verify backend is running on port 5000
- Check browser network tab for CORS errors
- Ensure SQLite database file has write permissions

## 📈 Future Enhancements

### **Planned Features**
- **Mobile App**: Native iOS and Android applications
- **Prescription History**: Long-term storage of user's prescription data
- **Doctor Integration**: API for healthcare provider systems
- **Advanced OCR**: Handwriting recognition for doctor prescriptions
- **Drug Information**: Detailed medicine information and dosage checking
- **Notification System**: Email/SMS alerts for new conflict discoveries

### **Technical Improvements**
- **Cloud Deployment**: AWS/Azure hosting for production use
- **Database Scaling**: PostgreSQL migration for enterprise use
- **API Rate Limiting**: Protection against abuse and overuse
- **Audit Logging**: Comprehensive logging for compliance
- **Backup System**: Automated database backups and recovery

## 📞 Support & Contributing

### **Getting Help**
- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check this README for detailed information
- **Community**: Join discussions and share feedback

### **Contributing**
- **Code Contributions**: Fork the repository and submit pull requests
- **Medical Database**: Help expand the drug interaction database
- **Testing**: Report bugs and suggest improvements
- **Documentation**: Improve guides and documentation

---

## 📄 License & Disclaimer

**Educational Purpose**: SPARD is designed for educational and informational purposes only.

**Medical Disclaimer**: This application is not a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical decisions.

**Liability**: The developers are not responsible for any medical decisions made based on SPARD's analysis.

---

*Made with ❤️ for healthcare safety and patient well-being* 
                "reason": "Aspirin enhances the blood-thinning effect of Warfarin, increasing bleeding risk."
            }
        ],
        "allergy_conflicts": [
            {
                "allergy": "salicylates", 
                "reason": "Aspirin is a salicylate and may trigger allergic reactions."
            }
        ]
    }
}
```

### 📊 Risk Level Calculation

```python
def _calculate_risk_level(self, interactions, allergy_conflicts):
    total_conflicts = len(interactions) + len(allergy_conflicts)
    
    if total_conflicts == 0:
        return "LOW"
    elif total_conflicts <= 2:
        # Check for high-severity keywords
        high_risk_keywords = ["bleeding", "severe", "toxicity", "serotonin syndrome"]
        
        for interaction in interactions:
            if any(keyword in interaction["reason"].lower() for keyword in high_risk_keywords):
                return "HIGH"
        
        # Allergies are generally high risk
        if len(allergy_conflicts) > 0:
            return "HIGH"
            
        return "MEDIUM"
    else:
        return "HIGH"
```

## 🧪 Testing

### Test the Backend

```powershell
cd backend
python conflict_checker.py
```

This runs built-in test cases showing different risk scenarios.

### Test with Sample Data

Open browser console and run:

```javascript
// Load sample data for testing
testWithSampleData();
```

This populates both doctors with sample medicines for immediate testing.

### Manual API Testing

```bash
curl -X POST http://localhost:5000/check-conflicts \
  -H "Content-Type: application/json" \
  -d '{
    "doctorA_medicines": ["metformin", "ibuprofen"],
    "doctorB_medicines": ["aspirin", "amoxicillin"]
  }'
```

## 🔧 API Endpoints

### POST /check-conflicts
Main endpoint for conflict analysis

**Request:**
```json
{
    "doctorA_medicines": ["metformin", "ibuprofen"],
    "doctorB_medicines": ["aspirin", "amoxicillin"]
}
```

**Response:**
```json
{
    "doctorA_medicines": ["metformin", "ibuprofen"],
    "doctorB_medicines": ["aspirin", "amoxicillin"],
    "interactions": [
        {
            "pair": "metformin + ibuprofen",
            "reason": "Ibuprofen can destabilize blood sugar levels when combined with Metformin."
        }
    ],
    "allergy_conflicts": [
        {
            "medicine": "amoxicillin",
            "allergy": "penicillin",
            "reason": "Amoxicillin belongs to the penicillin family and may cause severe allergic reactions."
        }
    ],
    "risk_level": "HIGH",
    "message": "Unsafe combination detected. Please consult your doctor before taking these medicines together."
}
```

### GET /medicines
Get all medicines in the database

### GET /conflicts/&lt;medicine&gt;
Get conflicts for a specific medicine

## 🎨 UI Features

- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **🎭 Drag & Drop**: Intuitive file upload interface
- **📊 Progress Tracking**: Real-time OCR processing feedback
- **🏷️ Medicine Tags**: Visual representation of extracted medicines
- **🚦 Risk Color Coding**: Clear visual risk indicators
- **💾 Auto-Save**: Automatic localStorage persistence
- **🔄 Real-time Updates**: Dynamic UI updates without page refresh

## ⚠️ Important Notes

1. **Medical Disclaimer**: This tool is for informational purposes only. Always consult healthcare professionals before making medication decisions.

2. **OCR Accuracy**: OCR results depend on image quality. For best results:
   - Use high-contrast, clear images
   - Ensure text is legible and well-lit
   - Avoid handwritten prescriptions when possible

3. **Database Coverage**: The conflict database includes 50+ common medicines. Not all possible medicines or interactions are included.

4. **Browser Compatibility**: Requires modern browsers supporting ES6+ features and Tesseract.js.

## 🔧 Troubleshooting

### OCR Not Working
- Check internet connection (Tesseract.js loads from CDN)
- Try a clearer, higher-resolution image
- Ensure image contains visible text

### Backend Connection Failed
- Verify Flask server is running on port 5000
- Check for CORS errors in browser console
- Ensure firewall allows connections to localhost:5000

### No Medicines Detected
- Image quality might be too low
- Try manually testing with sample data: `testWithSampleData()`
- Check browser console for OCR processing logs

## 🚀 Future Enhancements

- **📝 Manual Medicine Entry**: Allow users to manually add/edit medicines
- **🔍 Advanced OCR**: Better medicine name recognition and fuzzy matching
- **📊 Detailed Reports**: Downloadable PDF reports
- **🔐 User Accounts**: Save analysis history
- **🌍 Multi-language**: Support for multiple languages
- **📱 Mobile App**: Native mobile application
- **🔬 Extended Database**: More medicines and interaction types

## 📄 License

This project is for educational and informational purposes only. Not intended for production medical use without proper validation and regulatory approval.

---

**Built with ❤️ for safer medication management**