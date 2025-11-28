// Global variables
let doctorAMedicines = [];
let doctorBMedicines = [];
let userAllergies = [];
let isProcessingA = false;
let isProcessingB = false;

// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    checkAndLoadSavedData();
});

function initializeEventListeners() {
    console.log('DEBUG: Setting up event listeners');
    
    // File upload listeners
    document.getElementById('prescriptionA').addEventListener('change', handleFileUpload);
    document.getElementById('prescriptionB').addEventListener('change', handleFileUpload);
    
    // Drag and drop listeners
    setupDragAndDrop('uploadBoxA', 'prescriptionA');
    setupDragAndDrop('uploadBoxB', 'prescriptionB');
    
    // Allergy input listeners
    const addAllergyBtn = document.getElementById('addAllergyBtn');
    const allergyInput = document.getElementById('allergyInput');
    
    if (addAllergyBtn) {
        console.log('DEBUG: Setting up add allergy button listener');
        addAllergyBtn.addEventListener('click', addAllergy);
    } else {
        console.error('DEBUG: addAllergyBtn element not found!');
    }
    
    if (allergyInput) {
        console.log('DEBUG: Setting up allergy input keypress listener');
        allergyInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addAllergy();
            }
        });
    } else {
        console.error('DEBUG: allergyInput element not found!');
    }
    
    // Button listeners
    document.getElementById('checkConflicts').addEventListener('click', checkConflicts);
    document.getElementById('clearAll').addEventListener('click', clearAll);
    
    console.log('DEBUG: Event listeners setup completed');
}

function setupDragAndDrop(boxId, inputId) {
    const box = document.getElementById(boxId);
    const input = document.getElementById(inputId);
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        box.addEventListener(eventName, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(eventName => {
        box.addEventListener(eventName, () => box.classList.add('dragover'), false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        box.addEventListener(eventName, () => box.classList.remove('dragover'), false);
    });
    
    box.addEventListener('drop', function(e) {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            input.files = files;
            handleFileUpload({ target: input });
        }
    });
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    const isDocA = event.target.id === 'prescriptionA';
    
    if (!file) return;
    
    // Validate file type
    if (!file.type.match('image.*')) {
        alert('Please select an image file (PNG, JPG, JPEG)');
        return;
    }
    
    // Show preview
    showImagePreview(file, isDocA ? 'previewA' : 'previewB');
    
    // Start OCR processing
    performOCR(file, isDocA);
}

function showImagePreview(file, containerId) {
    const container = document.getElementById(containerId);
    const reader = new FileReader();
    
    reader.onload = function(e) {
        container.innerHTML = `<img src="${e.target.result}" alt="Prescription preview">`;
    };
    
    reader.readAsDataURL(file);
}

async function performOCR(file, isDocA) {
    const progressId = isDocA ? 'progressA' : 'progressB';
    const medicinesId = isDocA ? 'medicinesA' : 'medicinesB';
    const progressElement = document.getElementById(progressId);
    
    // Set processing flag
    if (isDocA) {
        isProcessingA = true;
    } else {
        isProcessingB = true;
    }
    
    // Show progress bar
    progressElement.style.display = 'block';
    progressElement.innerHTML = '<div class="progress-bar" style="width: 10%"></div>';
    
    try {
        console.log(`Starting OCR for Doctor ${isDocA ? 'A' : 'B'}...`);
        
        const { data: { text } } = await Tesseract.recognize(file, 'eng', {
            logger: m => {
                if (m.status === 'recognizing text') {
                    const progress = Math.round(m.progress * 100);
                    const progressBar = progressElement.querySelector('.progress-bar');
                    if (progressBar) {
                        progressBar.style.width = progress + '%';
                    }
                }
                console.log(`OCR Progress: ${m.status} - ${Math.round(m.progress * 100)}%`);
            }
        });
        
        console.log('OCR Text extracted:', text);
        
        // Extract medicines from text
        const medicines = extractMedicinesFromText(text);
        console.log('Extracted medicines:', medicines);
        
        // Store medicines
        if (isDocA) {
            doctorAMedicines = medicines;
            localStorage.setItem('doctorA', JSON.stringify(medicines));
            isProcessingA = false;
        } else {
            doctorBMedicines = medicines;
            localStorage.setItem('doctorB', JSON.stringify(medicines));
            isProcessingB = false;
        }
        
        // Display extracted medicines
        displayExtractedMedicines(medicines, medicinesId);
        
        // Hide progress bar
        progressElement.style.display = 'none';
        
        // Update check button state
        updateCheckButtonState();
        
    } catch (error) {
        console.error('OCR Error:', error);
        
        // Reset processing flag
        if (isDocA) {
            isProcessingA = false;
        } else {
            isProcessingB = false;
        }
        
        progressElement.innerHTML = '<div style="color: red; text-align: center;">OCR processing failed. Please try again.</div>';
        
        setTimeout(() => {
            progressElement.style.display = 'none';
        }, 3000);
    }
}

function extractMedicinesFromText(text) {
    // Updated medicine names database for better extraction
    const commonMedicines = [
        'metformin', 'ibuprofen', 'amoxicillin', 'paracetamol', 'aspirin', 
        'warfarin', 'azithromycin', 'cetirizine', 'pantoprazole', 'omeprazole',
        'clopidogrel', 'lisinopril', 'amlodipine', 'simvastatin', 'levocetirizine',
        'montelukast', 'diclofenac', 'sertraline', 'tramadol', 'metronidazole',
        'acetaminophen', 'cough_syrup', 'insulin', 'atenolol', 'erythromycin',
        'statins', 'ceftriaxone', 'doxycycline', 'antacids', 'prednisolone',
        'losartan', 'furosemide', 'gabapentin', 'citalopram', 'fluoxetine',
        'lansoprazole', 'esomeprazole', 'ranitidine', 'loratadine', 'glipizide',
        'glyburide', 'pioglitazone', 'metoprolol', 'propranolol', 'carvedilol',
        'digoxin', 'spironolactone', 'hydrochlorothiazide', 'prednisone',
        'dexamethasone', 'levothyroxine', 'albuterol', 'fluticasone', 'budesonide',
        'salbutamol', 'beclomethasone', 'beta_blockers', 'ace_inhibitors', 'macrolide'
    ];
    
    // Clean and normalize text
    const cleanText = text.toLowerCase()
        .replace(/[^a-z\s\n]/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
    
    const words = cleanText.split(/\s+/);
    const extractedMedicines = [];
    
    // Look for exact matches first
    commonMedicines.forEach(medicine => {
        if (words.includes(medicine) && !extractedMedicines.includes(medicine)) {
            extractedMedicines.push(medicine);
        }
    });
    
    // Look for partial matches (fuzzy matching)
    if (extractedMedicines.length === 0) {
        words.forEach(word => {
            if (word.length >= 4) {
                commonMedicines.forEach(medicine => {
                    if (medicine.includes(word) || word.includes(medicine.substring(0, 4))) {
                        if (!extractedMedicines.includes(medicine)) {
                            extractedMedicines.push(medicine);
                        }
                    }
                });
            }
        });
    }
    
    // If still no medicines found, try to extract medicine-like words
    if (extractedMedicines.length === 0) {
        words.forEach(word => {
            // Look for words that might be medicine names (length > 5, contains common medicine suffixes)
            if (word.length > 5 && 
                (word.endsWith('in') || word.endsWith('ol') || word.endsWith('pril') || 
                 word.endsWith('ine') || word.endsWith('ate') || word.endsWith('ide') ||
                 word.endsWith('mycin') || word.endsWith('azole') || word.endsWith('statin'))) {
                extractedMedicines.push(word);
            }
        });
    }
    
    return extractedMedicines.slice(0, 10); // Limit to 10 medicines to avoid noise
}

function displayExtractedMedicines(medicines, containerId) {
    const container = document.getElementById(containerId);
    
    if (medicines.length === 0) {
        container.innerHTML = `
            <h3>⚠️ No medicines detected</h3>
            <p>The OCR could not detect any medicines. You can manually add them if needed.</p>
        `;
    } else {
        const medicinesList = medicines.map(medicine => 
            `<span class="medicine-tag">${medicine}</span>`
        ).join('');
        
        container.innerHTML = `
            <h3>💊 Detected Medicines (${medicines.length})</h3>
            <div class="medicine-list">${medicinesList}</div>
        `;
    }
    
    container.style.display = 'block';
}

function updateCheckButtonState() {
    const checkButton = document.getElementById('checkConflicts');
    const hasDataFromBoth = doctorAMedicines.length > 0 && doctorBMedicines.length > 0;
    const notProcessing = !isProcessingA && !isProcessingB;
    
    checkButton.disabled = !(hasDataFromBoth && notProcessing);
}

async function checkConflicts() {
    if (doctorAMedicines.length === 0 || doctorBMedicines.length === 0) {
        alert('Please upload and process both prescription images first.');
        return;
    }
    
    // Show loading
    document.getElementById('loadingSection').style.display = 'flex';
    
    try {
        const requestData = {
            doctorA_medicines: doctorAMedicines,
            doctorB_medicines: doctorBMedicines
        };
        
        // Include user allergies if any
        if (userAllergies.length > 0) {
            requestData.user_allergies = userAllergies;
            console.log('DEBUG: Sending user allergies:', userAllergies);
        } else {
            console.log('DEBUG: No user allergies to send');
        }
        
        console.log('DEBUG: Full request data:', requestData);
        
        const response = await fetch(`${API_BASE_URL}/check-conflicts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const results = await response.json();
        displayResults(results);
        
    } catch (error) {
        console.error('Error checking conflicts:', error);
        alert('Error communicating with the server. Please ensure the Flask backend is running on port 5000.');
    } finally {
        // Hide loading
        document.getElementById('loadingSection').style.display = 'none';
    }
}

function displayResults(results) {
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    
    let html = '';
    
    // Display medicines found
    html += `
        <div class="result-item medicines-found">
            <h3>💊 Medicines Found</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4>Doctor A:</h4>
                    <div class="medicine-list">
                        ${results.doctorA_medicines.map(med => `<span class="medicine-tag">${med}</span>`).join('')}
                    </div>
                </div>
                <div>
                    <h4>Doctor B:</h4>
                    <div class="medicine-list">
                        ${results.doctorB_medicines.map(med => `<span class="medicine-tag">${med}</span>`).join('')}
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Display drug interactions
    if (results.interactions && results.interactions.length > 0) {
        html += `
            <div class="result-item interactions">
                <h3>⚠️ Drug Interactions Found (${results.interactions.length})</h3>
                ${results.interactions.map(interaction => `
                    <div class="conflict-item">
                        <div class="conflict-pair">${interaction.pair}</div>
                        <div class="conflict-reason">${interaction.reason}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    // Display user allergy conflicts (only show if user allergies match dataset)
    if (results.allergy_conflicts && results.allergy_conflicts.length > 0) {
        html += `
            <div class="result-item allergy-conflicts user-allergy">
                <h3>⚠️ Your Allergy Conflicts Found (${results.allergy_conflicts.length})</h3>
                <p style="font-size: 0.9em; color: #dc3545; margin-bottom: 15px; font-weight: bold;">Your allergies match contraindications in our database</p>
                ${results.allergy_conflicts.map(allergy => `
                    <div class="conflict-item urgent">
                        <div class="conflict-pair">${allergy.medicine} ↔ ${allergy.allergy}</div>
                        <div class="conflict-reason">${allergy.reason}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    // Display risk level
    html += `
        <div class="result-item risk-level">
            <h3>📊 Risk Assessment</h3>
            <div class="risk-${results.risk_level.toLowerCase()}">${results.risk_level} RISK</div>
            <p style="margin-top: 15px; font-size: 1.1rem; line-height: 1.6;">
                <strong>${results.message}</strong>
            </p>
        </div>
    `;
    
    // If no conflicts found
    if (results.interactions.length === 0 && results.allergy_conflicts.length === 0) {
        html += `
            <div class="result-item medicines-found">
                <h3>✅ No Conflicts Detected</h3>
                <p>Based on our database, no drug interactions or allergy conflicts were found between these prescriptions and your known allergies.</p>
                <p><em>Note: This is not a substitute for professional medical advice. Always consult your healthcare provider.</em></p>
            </div>
        `;
    }
    
    resultsContent.innerHTML = html;
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function clearAll() {
    if (confirm('Are you sure you want to clear all data? This will remove uploaded images and extracted medicines.')) {
        // Use the centralized clear function
        clearAllMedicineData();
        
        // Reset processing states
        isProcessingA = false;
        isProcessingB = false;
        
        // Clear file inputs
        document.getElementById('prescriptionA').value = '';
        document.getElementById('prescriptionB').value = '';
        
        // Clear previews
        document.getElementById('previewA').innerHTML = '';
        document.getElementById('previewB').innerHTML = '';
        
        // Hide progress bars
        document.getElementById('progressA').style.display = 'none';
        document.getElementById('progressB').style.display = 'none';
        
        // Reset upload boxes
        document.getElementById('uploadBoxA').classList.remove('dragover');
        document.getElementById('uploadBoxB').classList.remove('dragover');
    }
}

function checkAndLoadSavedData() {
    console.log('DEBUG: checkAndLoadSavedData called');
    
    // Check if this is a fresh login by comparing session info
    const currentUser = JSON.parse(localStorage.getItem('currentUser') || 'null');
    const lastSessionId = localStorage.getItem('lastSessionId');
    
    console.log('DEBUG: Current user:', currentUser);
    console.log('DEBUG: Last session ID:', lastSessionId);
    
    if (currentUser && currentUser.session_id) {
        if (lastSessionId !== currentUser.session_id) {
            console.log('DEBUG: Fresh login detected - clearing old data');
            // Fresh login - clear old medicine data but NOT allergies (user might want to keep them)
            clearMedicineData();
            localStorage.setItem('lastSessionId', currentUser.session_id);
        } else {
            console.log('DEBUG: Same session - loading saved data');
            // Same session - load saved medicines and allergies
            loadSavedMedicines();
        }
        // Always load allergies regardless of session
        loadSavedAllergies();
    } else {
        console.log('DEBUG: No user logged in - clearing everything');
        // No user logged in - clear everything
        clearAllMedicineData();
        localStorage.removeItem('lastSessionId');
    }
    
    console.log('DEBUG: Final userAllergies array:', userAllergies);
}

function addAllergy() {
    console.log('DEBUG: addAllergy function called');
    
    const allergyInput = document.getElementById('allergyInput');
    const allergyName = allergyInput.value.trim();
    
    console.log('DEBUG: Allergy input value:', allergyName);
    
    if (!allergyName) {
        console.log('DEBUG: No allergy name entered');
        alert('Please enter an allergy name');
        return;
    }
    
    // Check if allergy already exists
    if (userAllergies.some(allergy => allergy.toLowerCase() === allergyName.toLowerCase())) {
        console.log('DEBUG: Allergy already exists');
        alert('This allergy is already in your list');
        allergyInput.value = '';
        return;
    }
    
    // Add allergy to list
    userAllergies.push(allergyName);
    console.log('DEBUG: Added allergy. Current list:', userAllergies);
    
    // Save to localStorage
    localStorage.setItem('userAllergies', JSON.stringify(userAllergies));
    console.log('DEBUG: Saved to localStorage');
    
    // Update display
    displayAllergies();
    console.log('DEBUG: Updated display');
    
    // Clear input
    allergyInput.value = '';
    
    // Update check button state
    updateCheckButtonState();
    console.log('DEBUG: addAllergy function completed');
}

function removeAllergy(allergyToRemove) {
    userAllergies = userAllergies.filter(allergy => allergy !== allergyToRemove);
    
    // Save to localStorage
    localStorage.setItem('userAllergies', JSON.stringify(userAllergies));
    
    // Update display
    displayAllergies();
    
    // Update check button state
    updateCheckButtonState();
}

function displayAllergies() {
    console.log('DEBUG: displayAllergies called with:', userAllergies);
    
    const allergiesDisplay = document.getElementById('allergiesDisplay');
    
    if (!allergiesDisplay) {
        console.error('DEBUG: allergiesDisplay element not found!');
        return;
    }
    
    if (userAllergies.length === 0) {
        console.log('DEBUG: No allergies to display');
        allergiesDisplay.classList.remove('show');
        return;
    }
    
    allergiesDisplay.classList.add('show');
    
    const allergiesHtml = `
        <h4>📋 Your Allergies:</h4>
        <div class="allergies-list">
            ${userAllergies.map(allergy => `
                <div class="allergy-tag">
                    ${allergy}
                    <button class="remove-allergy" onclick="removeAllergy('${allergy}')" title="Remove allergy">
                        ×
                    </button>
                </div>
            `).join('')}
        </div>
    `;
    
    allergiesDisplay.innerHTML = allergiesHtml;
    console.log('DEBUG: Allergies display updated with HTML:', allergiesHtml);
}

function loadSavedAllergies() {
    console.log('DEBUG: loadSavedAllergies called');
    
    const savedAllergies = localStorage.getItem('userAllergies');
    console.log('DEBUG: Raw saved allergies from localStorage:', savedAllergies);
    
    if (savedAllergies) {
        try {
            userAllergies = JSON.parse(savedAllergies);
            console.log('DEBUG: Parsed user allergies:', userAllergies);
            displayAllergies();
        } catch (e) {
            console.error('Error loading saved allergies:', e);
            userAllergies = [];
        }
    } else {
        console.log('DEBUG: No saved allergies found in localStorage');
        userAllergies = [];
    }
    
    console.log('DEBUG: Final userAllergies array after loading:', userAllergies);
}

function clearMedicineData() {
    console.log('DEBUG: clearMedicineData called');
    
    // Clear only medicine arrays (preserve allergies)
    doctorAMedicines = [];
    doctorBMedicines = [];
    
    // Clear only medicine localStorage
    localStorage.removeItem('doctorA');
    localStorage.removeItem('doctorB');
    
    // Clear medicine UI displays
    const medicinesADiv = document.getElementById('medicinesA');
    const medicinesBDiv = document.getElementById('medicinesB');
    
    if (medicinesADiv) {
        medicinesADiv.innerHTML = '';
        medicinesADiv.style.display = 'none';
    }
    
    if (medicinesBDiv) {
        medicinesBDiv.innerHTML = '';
        medicinesBDiv.style.display = 'none';
    }
    
    // Update button state
    updateCheckButtonState();
    
    // Hide results if shown
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.style.display = 'none';
    }
    
    console.log('DEBUG: Medicine data cleared');
}

function clearAllMedicineData() {
    console.log('DEBUG: clearAllMedicineData called');
    
    // Clear arrays
    doctorAMedicines = [];
    doctorBMedicines = [];
    userAllergies = [];
    
    // Clear localStorage
    localStorage.removeItem('doctorA');
    localStorage.removeItem('doctorB');
    localStorage.removeItem('userAllergies');
    
    // Clear UI displays
    const medicinesADiv = document.getElementById('medicinesA');
    const medicinesBDiv = document.getElementById('medicinesB');
    const allergiesDisplay = document.getElementById('allergiesDisplay');
    
    if (medicinesADiv) {
        medicinesADiv.innerHTML = '';
        medicinesADiv.style.display = 'none';
    }
    
    if (medicinesBDiv) {
        medicinesBDiv.innerHTML = '';
        medicinesBDiv.style.display = 'none';
    }
    
    if (allergiesDisplay) {
        allergiesDisplay.innerHTML = '';
        allergiesDisplay.classList.remove('show');
    }
    
    // Clear allergy input
    const allergyInput = document.getElementById('allergyInput');
    if (allergyInput) {
        allergyInput.value = '';
    }
    
    // Update button state
    updateCheckButtonState();
    
    // Hide results if shown
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.style.display = 'none';
    }
    
    console.log('DEBUG: All data cleared');
}

function loadSavedMedicines() {
    // Load previously extracted medicines from localStorage
    const savedDoctorA = localStorage.getItem('doctorA');
    const savedDoctorB = localStorage.getItem('doctorB');
    
    if (savedDoctorA) {
        try {
            doctorAMedicines = JSON.parse(savedDoctorA);
            if (doctorAMedicines.length > 0) {
                displayExtractedMedicines(doctorAMedicines, 'medicinesA');
            }
        } catch (e) {
            console.error('Error loading saved Doctor A medicines:', e);
        }
    }
    
    if (savedDoctorB) {
        try {
            doctorBMedicines = JSON.parse(savedDoctorB);
            if (doctorBMedicines.length > 0) {
                displayExtractedMedicines(doctorBMedicines, 'medicinesB');
            }
        } catch (e) {
            console.error('Error loading saved Doctor B medicines:', e);
        }
    }
    
    updateCheckButtonState();
}

// Utility function to test OCR with sample medicines
function testWithSampleData() {
    // For testing purposes - you can call this from browser console
    doctorAMedicines = ['metformin', 'ibuprofen'];
    doctorBMedicines = ['aspirin', 'amoxicillin'];
    
    localStorage.setItem('doctorA', JSON.stringify(doctorAMedicines));
    localStorage.setItem('doctorB', JSON.stringify(doctorBMedicines));
    
    displayExtractedMedicines(doctorAMedicines, 'medicinesA');
    displayExtractedMedicines(doctorBMedicines, 'medicinesB');
    
    updateCheckButtonState();
    
    console.log('Sample data loaded for testing');
}

// Make testWithSampleData available globally for debugging
window.testWithSampleData = testWithSampleData;