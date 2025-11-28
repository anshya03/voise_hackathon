"""
Prescription Conflict Checker
Analyzes drug-drug interactions and allergy conflicts between prescriptions
"""

import json
from typing import List, Dict, Any, Optional, Tuple

class ConflictChecker:
    def __init__(self):
        """Initialize the conflict checker with the complete conflict database"""
        self.conflict_database = {
            "lisinopril": {
                "conflicts": [
                    {"drug": "atenolol", "reason": "Combining ACE inhibitors with beta-blockers requires careful blood pressure monitoring."},
                    {"drug": "ibuprofen", "reason": "Ibuprofen may reduce the blood pressure-lowering effect of Lisinopril."}
                ],
                "allergy_conflicts": [
                    {"allergy": "ace_inhibitors", "reason": "Lisinopril is an ACE inhibitor and may trigger reactions."}
                ]
            },

            "metformin": {
                "conflicts": [
                    {"drug": "ibuprofen", "reason": "Ibuprofen can destabilize blood sugar levels when combined with Metformin."}
                ],
                "allergy_conflicts": [
                    {"allergy": "metformin", "reason": "You are allergic to Metformin. This diabetes medication should be avoided."},
                    {"allergy": "biguanide", "reason": "Metformin is a biguanide medication and should be avoided by people with biguanide allergies."}
                ]
            },

            "aspirin": {
                "conflicts": [
                    {"drug": "ibuprofen", "reason": "Taking both aspirin and ibuprofen together can increase stomach bleeding risk."}
                ],
                "allergy_conflicts": [
                    {"allergy": "aspirin", "reason": "You are allergic to aspirin. Taking this medication can cause severe allergic reactions."},
                    {"allergy": "salicylate", "reason": "Aspirin contains salicylates and should be avoided by people with salicylate allergies."},
                    {"allergy": "nsaid", "reason": "Aspirin is an NSAID and should be avoided by people with NSAID allergies."}
                ]
            },

            "ibuprofen": {
                "conflicts": [
                    {"drug": "metformin", "reason": "This combination can cause blood sugar fluctuations and stomach issues."},
                    {"drug": "aspirin", "reason": "Both are NSAIDs and can increase stomach bleeding risk."}
                ],
                "allergy_conflicts": [
                    {"allergy": "nsaid", "reason": "Ibuprofen is an NSAID and should be avoided by people with NSAID allergies."}
                ]
            },

            "amoxicillin": {
                "conflicts": [],
                "allergy_conflicts": [
                    {"allergy": "penicillin", "reason": "Amoxicillin belongs to the penicillin family and may cause severe allergic reactions."}
                ]
            },

            "paracetamol": {
                "conflicts": [
                    {"drug": "alcohol", "reason": "This combination increases the risk of liver damage."}
                ],
                "allergy_conflicts": []
            },

            "aspirin": {
                "conflicts": [
                    {"drug": "ibuprofen", "reason": "Both are NSAIDs and may cause internal bleeding when taken together."},
                    {"drug": "warfarin", "reason": "Aspirin enhances the blood-thinning effect of Warfarin, increasing bleeding risk."}
                ],
                "allergy_conflicts": [
                    {"allergy": "salicylates", "reason": "Aspirin is a salicylate and may trigger allergic reactions."}
                ]
            },

            "warfarin": {
                "conflicts": [
                    {"drug": "aspirin", "reason": "Both thin the blood and may cause severe bleeding."},
                    {"drug": "ibuprofen", "reason": "NSAIDs can increase bleeding when combined with Warfarin."}
                ],
                "allergy_conflicts": []
            },

            "azithromycin": {
                "conflicts": [
                    {"drug": "antacids", "reason": "Antacids reduce the absorption of Azithromycin."}
                ],
                "allergy_conflicts": [
                    {"allergy": "macrolide", "reason": "Azithromycin is a macrolide antibiotic and may cause allergic reactions."}
                ]
            },

            "cetirizine": {
                "conflicts": [
                    {"drug": "alcohol", "reason": "Alcohol increases drowsiness when taken with Cetirizine."}
                ],
                "allergy_conflicts": []
            },

            "pantoprazole": {
                "conflicts": [],
                "allergy_conflicts": []
            },

            "omeprazole": {
                "conflicts": [
                    {"drug": "clopidogrel", "reason": "Omeprazole reduces the activation of Clopidogrel, lowering its effectiveness."}
                ],
                "allergy_conflicts": []
            },

            "clopidogrel": {
                "conflicts": [
                    {"drug": "omeprazole", "reason": "Omeprazole reduces how well Clopidogrel works."}
                ],
                "allergy_conflicts": []
            },

            "simvastatin": {
                "conflicts": [
                    {"drug": "warfarin", "reason": "Simvastatin can enhance the blood-thinning effect of Warfarin."}
                ],
                "allergy_conflicts": []
            },

            "amlodipine": {
                "conflicts": [
                    {"drug": "simvastatin", "reason": "High doses of Simvastatin with Amlodipine may cause muscle damage."}
                ],
                "allergy_conflicts": []
            },

            "simvastatin": {
                "conflicts": [
                    {"drug": "amlodipine", "reason": "Combination may increase risk of muscle breakdown."}
                ],
                "allergy_conflicts": []
            },

            "levocetirizine": {
                "conflicts": [
                    {"drug": "alcohol", "reason": "Increases drowsiness and dizziness."}
                ],
                "allergy_conflicts": []
            },

            "montelukast": {
                "conflicts": [],
                "allergy_conflicts": []
            },

            "diclofenac": {
                "conflicts": [
                    {"drug": "warfarin", "reason": "Increases risk of severe bleeding."}
                ],
                "allergy_conflicts": []
            },

            "sertraline": {
                "conflicts": [
                    {"drug": "tramadol", "reason": "May cause serotonin syndrome."}
                ],
                "allergy_conflicts": []
            },

            "tramadol": {
                "conflicts": [
                    {"drug": "sertraline", "reason": "May trigger serotonin syndrome, a life-threatening condition."}
                ],
                "allergy_conflicts": []
            },

            "metronidazole": {
                "conflicts": [
                    {"drug": "alcohol", "reason": "Causes severe vomiting and rapid heartbeat."}
                ],
                "allergy_conflicts": []
            },

            "acetaminophen": {
                "conflicts": [
                    {"drug": "alcohol", "reason": "Drastically increases risk of liver toxicity."}
                ],
                "allergy_conflicts": []
            },

            "cough_syrup": {
                "conflicts": [
                    {"drug": "paracetamol", "reason": "Many syrups contain paracetamol, increasing overdose risk."}
                ],
                "allergy_conflicts": []
            },

            "insulin": {
                "conflicts": [
                    {"drug": "beta_blockers", "reason": "Beta-blockers may hide symptoms of low blood sugar."}
                ],
                "allergy_conflicts": []
            },

            "atenolol": {
                "conflicts": [
                    {"drug": "insulin", "reason": "Masks signs of hypoglycemia."}
                ],
                "allergy_conflicts": []
            },

            "erythromycin": {
                "conflicts": [
                    {"drug": "statins", "reason": "May increase risk of muscle injury."}
                ],
                "allergy_conflicts": [
                    {"allergy": "macrolide", "reason": "Erythromycin is a macrolide and may cause allergic reactions."}
                ]
            },

            "statins": {
                "conflicts": [
                    {"drug": "erythromycin", "reason": "Increases statin concentration causing muscle damage."}
                ],
                "allergy_conflicts": []
            },

            "ceftriaxone": {
                "conflicts": [],
                "allergy_conflicts": [
                    {"allergy": "cephalosporin", "reason": "Ceftriaxone is a cephalosporin and may cause reactions."}
                ]
            },

            "doxycycline": {
                "conflicts": [
                    {"drug": "antacids", "reason": "Antacids reduce the absorption of Doxycycline."}
                ],
                "allergy_conflicts": []
            },

            "antacids": {
                "conflicts": [
                    {"drug": "doxycycline", "reason": "Reduces antibiotic absorption significantly."}
                ],
                "allergy_conflicts": []
            },

            "prednisolone": {
                "conflicts": [
                    {"drug": "ibuprofen", "reason": "Combination increases chances of stomach bleeding."}
                ],
                "allergy_conflicts": []
            }
        }

    def analyze_prescriptions(self, doctor_a_medicines: List[str], doctor_b_medicines: List[str], user_allergies: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Main method to analyze prescriptions from two doctors
        
        Args:
            doctor_a_medicines: List of medicines from Doctor A
            doctor_b_medicines: List of medicines from Doctor B
            user_allergies: Optional list of user's known allergies
            
        Returns:
            Complete analysis result in the specified format
        """
        user_allergies = user_allergies or []
        
        # Combine all medicines
        all_medicines = list(set(doctor_a_medicines + doctor_b_medicines))
        
        # Find drug-drug interactions
        interactions = self._find_drug_interactions(all_medicines)
        
        # Find user allergy conflicts (only show if user has matching allergies)
        user_allergy_conflicts = self._find_user_allergy_conflicts(all_medicines, user_allergies)
        
        # Calculate risk level
        risk_level = self._calculate_risk_level(interactions, user_allergy_conflicts)
        
        # Generate message
        message = self._generate_message(risk_level, interactions, user_allergy_conflicts)
        
        # Return result in exact format specified
        return {
            "doctorA_medicines": doctor_a_medicines,
            "doctorB_medicines": doctor_b_medicines,
            "interactions": interactions,
            "allergy_conflicts": user_allergy_conflicts,  # Only show user allergy conflicts
            "user_allergies": user_allergies,
            "risk_level": risk_level,
            "message": message
        }

    def _find_drug_interactions(self, medicines: List[str]) -> List[Dict[str, str]]:
        """Find all drug-drug interactions among the medicines"""
        interactions = []
        
        # Check each pair of medicines
        for i, med1 in enumerate(medicines):
            for j, med2 in enumerate(medicines):
                if i >= j:  # Avoid duplicates and self-comparison
                    continue
                
                # Check if med1 has conflicts with med2
                if med1 in self.conflict_database:
                    for conflict in self.conflict_database[med1]["conflicts"]:
                        if conflict["drug"] == med2:
                            interactions.append({
                                "pair": f"{med1} + {med2}",
                                "reason": conflict["reason"]
                            })
                
                # Check if med2 has conflicts with med1 (to catch bidirectional conflicts)
                if med2 in self.conflict_database:
                    for conflict in self.conflict_database[med2]["conflicts"]:
                        if conflict["drug"] == med1:
                            # Check if we already added this interaction
                            existing_pair = f"{med1} + {med2}"
                            reverse_pair = f"{med2} + {med1}"
                            
                            if not any(interaction["pair"] in [existing_pair, reverse_pair] 
                                     for interaction in interactions):
                                interactions.append({
                                    "pair": f"{med2} + {med1}",
                                    "reason": conflict["reason"]
                                })
        
        return interactions

    def _find_user_allergy_conflicts(self, medicines: List[str], user_allergies: List[str]) -> List[Dict[str, str]]:
        """
        Find conflicts between prescribed medicines and user's known allergies
        Only reports conflicts if the user's allergy matches the medicine's allergy profile in the dataset
        
        Args:
            medicines: List of prescribed medicines
            user_allergies: List of user's known allergies
            
        Returns:
            List of allergy conflicts found
        """
        conflicts = []
        
        print(f"DEBUG: Checking user allergies: {user_allergies}")
        print(f"DEBUG: Against medicines: {medicines}")
        
        if not user_allergies:
            print("DEBUG: No user allergies provided")
            return conflicts
        
        # Normalize user allergies for comparison
        normalized_user_allergies = [allergy.lower().strip() for allergy in user_allergies]
        print(f"DEBUG: Normalized user allergies: {normalized_user_allergies}")
        
        for medicine in medicines:
            medicine_lower = medicine.lower().strip()
            print(f"DEBUG: Checking medicine: {medicine_lower}")
            
            # Check if medicine exists in our conflict database
            if medicine_lower in self.conflict_database:
                medicine_data = self.conflict_database[medicine_lower]
                
                # Get the allergy conflicts defined for this medicine in the dataset
                dataset_allergies = medicine_data.get('allergy_conflicts', [])
                print(f"DEBUG: Dataset allergies for {medicine_lower}: {dataset_allergies}")
                
                # Check if any of the user's allergies match the dataset allergies for this medicine
                for dataset_allergy_info in dataset_allergies:
                    dataset_allergy = dataset_allergy_info.get('allergy', '').lower().strip()
                    print(f"DEBUG: Checking dataset allergy: {dataset_allergy}")
                    
                    # Check if user has this specific allergy - EXACT MATCH ONLY
                    for user_allergy in user_allergies:
                        user_allergy_lower = user_allergy.lower().strip()
                        print(f"DEBUG: Comparing user allergy '{user_allergy_lower}' with dataset allergy '{dataset_allergy}'")
                        
                        # Exact match only - no partial matching
                        if user_allergy_lower == dataset_allergy:
                            print(f"DEBUG: MATCH FOUND! {user_allergy_lower} == {dataset_allergy}")
                            conflicts.append({
                                "medicine": medicine,
                                "allergy": user_allergy,
                                "reason": dataset_allergy_info.get('reason', f"You are allergic to {user_allergy}. The prescribed medicine {medicine} is contraindicated for this allergy."),
                                "type": "user_allergy_dataset_match"
                            })
                            break  # Avoid duplicate conflicts for the same medicine
                        else:
                            print(f"DEBUG: No match: '{user_allergy_lower}' != '{dataset_allergy}'")
            else:
                print(f"DEBUG: Medicine {medicine_lower} not found in database")
        
        print(f"DEBUG: Final conflicts found: {conflicts}")
        return conflicts

    def _find_allergy_conflicts(self, medicines: List[str]) -> List[Dict[str, str]]:
        """Find all allergy conflicts among the medicines"""
        allergy_conflicts = []
        
        for medicine in medicines:
            if medicine in self.conflict_database:
                for allergy_conflict in self.conflict_database[medicine]["allergy_conflicts"]:
                    allergy_conflicts.append({
                        "medicine": medicine,
                        "allergy": allergy_conflict["allergy"],
                        "reason": allergy_conflict["reason"]
                    })
        
        return allergy_conflicts

    def _calculate_risk_level(self, interactions: List[Dict], allergy_conflicts: List[Dict]) -> str:
        """Calculate the overall risk level based on interactions and allergy conflicts"""
        total_conflicts = len(interactions) + len(allergy_conflicts)
        
        # Define risk criteria
        if total_conflicts == 0:
            return "LOW"
        elif total_conflicts <= 2:
            # Check for high-severity interactions
            high_risk_keywords = [
                "bleeding", "blood", "severe", "dangerous", "toxicity", 
                "serotonin syndrome", "hyperkalemia", "hypoglycemia",
                "rhabdomyolysis", "liver damage", "heart", "respiratory"
            ]
            
            # Check interactions for high-risk keywords
            for interaction in interactions:
                reason = interaction["reason"].lower()
                if any(keyword in reason for keyword in high_risk_keywords):
                    return "HIGH"
            
            # Check allergy conflicts (allergies are generally high risk)
            if len(allergy_conflicts) > 0:
                return "HIGH"
            
            return "MEDIUM"
        else:
            return "HIGH"

    def _generate_message(self, risk_level: str, interactions: List[Dict], allergy_conflicts: List[Dict]) -> str:
        """Generate appropriate message based on risk level and conflicts found"""
        if risk_level == "HIGH":
            if len(allergy_conflicts) > 0 and len(interactions) > 0:
                return "CRITICAL: Both drug interactions and allergy conflicts detected. Immediate medical consultation required before taking these medicines."
            elif len(allergy_conflicts) > 0:
                return "CRITICAL: Allergy conflicts detected. These medicines may cause severe allergic reactions. Consult your doctor immediately."
            else:
                return "Unsafe combination detected. Please consult your doctor before taking these medicines together."
        
        elif risk_level == "MEDIUM":
            return "Moderate risk detected. Monitor for side effects and consult your healthcare provider if you experience any unusual symptoms."
        
        else:  # LOW risk
            if len(interactions) == 0 and len(allergy_conflicts) == 0:
                return "No known conflicts detected between these medicines. Continue taking as prescribed, but always consult your healthcare provider for any concerns."
            else:
                return "Low risk combination. Monitor for any side effects and maintain regular follow-up with your healthcare provider."

    def get_all_known_medicines(self) -> List[str]:
        """Get list of all medicines in the conflict database"""
        return list(self.conflict_database.keys())

    def get_medicine_conflicts(self, medicine: str) -> Optional[Dict]:
        """Get all conflicts for a specific medicine"""
        medicine = medicine.lower().strip()
        return self.conflict_database.get(medicine)

    def add_medicine_to_database(self, medicine: str, conflicts: List[Dict], allergy_conflicts: List[Dict]):
        """Add a new medicine to the conflict database (for future expansion)"""
        medicine = medicine.lower().strip()
        self.conflict_database[medicine] = {
            "conflicts": conflicts,
            "allergy_conflicts": allergy_conflicts
        }

    def export_database(self) -> str:
        """Export the conflict database as JSON string"""
        return json.dumps(self.conflict_database, indent=2)

    def import_database(self, json_data: str):
        """Import conflict database from JSON string"""
        try:
            self.conflict_database = json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}")

# Example usage and testing
if __name__ == "__main__":
    # Initialize the conflict checker
    checker = ConflictChecker()
    
    # Test with sample data
    test_cases = [
        {
            "name": "High Risk Case",
            "doctor_a": ["metformin", "ibuprofen"],
            "doctor_b": ["aspirin", "amoxicillin"]
        },
        {
            "name": "Medium Risk Case",
            "doctor_a": ["omeprazole"],
            "doctor_b": ["lansoprazole"]
        },
        {
            "name": "No Risk Case",
            "doctor_a": ["cetirizine"],
            "doctor_b": ["levothyroxine"]
        }
    ]
    
    print("🏥 PRESCRIPTION CONFLICT CHECKER - TEST RESULTS")
    print("=" * 60)
    
    for test_case in test_cases:
        print(f"\n📋 TEST CASE: {test_case['name']}")
        print(f"Doctor A: {test_case['doctor_a']}")
        print(f"Doctor B: {test_case['doctor_b']}")
        print("-" * 40)
        
        result = checker.analyze_prescriptions(test_case['doctor_a'], test_case['doctor_b'])
        
        print(f"💊 RISK LEVEL: {result['risk_level']}")
        print(f"📝 MESSAGE: {result['message']}")
        
        if result['interactions']:
            print(f"⚠️  INTERACTIONS FOUND: {len(result['interactions'])}")
            for interaction in result['interactions']:
                print(f"   • {interaction['pair']}: {interaction['reason']}")
        
        if result['allergy_conflicts']:
            print(f"🚨 ALLERGY CONFLICTS: {len(result['allergy_conflicts'])}")
            for allergy in result['allergy_conflicts']:
                print(f"   • {allergy['medicine']} ({allergy['allergy']}): {allergy['reason']}")
        
        print()
    
    print("✅ All test cases completed!")
    print(f"📊 Total medicines in database: {len(checker.get_all_known_medicines())}")