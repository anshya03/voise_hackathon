# Allergy Detection Test Examples

## Current Dataset Allergies:

### Lisinopril
- **Allergy**: `ace_inhibitors`
- **Reason**: "Lisinopril is an ACE inhibitor and may trigger reactions."

### Ibuprofen  
- **Allergy**: `nsaid`
- **Reason**: "Ibuprofen is an NSAID and should be avoided by people with NSAID allergies."

## Test Scenarios:

### ✅ EXACT MATCH - Will Detect Conflict
- **User enters**: "ace_inhibitors"
- **Medicine**: "lisinopril"
- **Result**: ❌ **CONFLICT DETECTED** (exact match)

### ✅ EXACT MATCH - Will Detect Conflict
- **User enters**: "nsaid"
- **Medicine**: "ibuprofen" 
- **Result**: ❌ **CONFLICT DETECTED** (exact match)

### ❌ NO MATCH - Will NOT Detect Conflict
- **User enters**: "penicillin"
- **Medicine**: "lisinopril"
- **Result**: ✅ **NO CONFLICT** (penicillin not in lisinopril's allergy list)

### ❌ NO MATCH - Will NOT Detect Conflict
- **User enters**: "shellfish"
- **Medicine**: "ibuprofen"
- **Result**: ✅ **NO CONFLICT** (shellfish not in ibuprofen's allergy list)

### ❌ NO MATCH - Will NOT Detect Conflict
- **User enters**: "ace"
- **Medicine**: "lisinopril"
- **Result**: ✅ **NO CONFLICT** ("ace" ≠ "ace_inhibitors" - exact match required)

## User Allergies Storage:
- Saved to localStorage as `userAllergies`
- Persists across sessions
- Cleared on logout or fresh login
- Retrieved from localStorage on page load