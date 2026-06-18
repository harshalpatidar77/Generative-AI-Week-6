# simple medical agent project 
# Features - Patient Register karega, Previous history load karega, Symptom store karega, LLM analyze karega,   
# Features - Strict JSON output lega, JSON save karega, Conversation save karega, 
# Features - Ek baar run hoke automatically exit ho jayega. 
import json
import os
import re
from datetime import datetime 
from dotenv import load_dotenv
from langchain_groq import ChatGroq  
# LOAD ENV 
load_dotenv() 
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
) 
# MEMORY FILE 
MEMORY_FILE = "patient_records.json" 
def load_records(): 
    if os.path.exists(MEMORY_FILE): 
        with open(MEMORY_FILE, "r") as f:
            return json.load(f) 
    return {} 
def save_records(records): 
    with open(MEMORY_FILE, "w") as f:
        json.dump(records, f, indent=4) 
records = load_records()  
# PATIENT REGISTRATION  
patient_name = input("Enter Patient Name: ").strip() 
if patient_name not in records: 
    age = input("Age: ")
    gender = input("Gender: ") 
    records[patient_name] = { 
        "patient_info": {
            "age": age,
            "gender": gender
        }, 
        "symptoms": [],
        "medicine_history": [],
        "conversation": []
    } 
    save_records(records) 
    print(f"\nNew Patient Registered: {patient_name}") 
else: 
    print(f"\nWelcome Back {patient_name}")  
# MEMORY CONTEXT 
def get_patient_context(): 
    patient = records[patient_name] 
    return json.dumps(
        {
            "symptoms": patient["symptoms"],
            "medicine_history":
                patient["medicine_history"]
        },
        indent=2
    )  
# STORE SYMPTOM 
def save_symptom(symptom): 
    symptom_data = { 
        "date":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ), 
        "symptom":
            symptom
    } 
    records[patient_name]["symptoms"].append(
        symptom_data
    ) 
    save_records(records) 
    print("[DEBUG] Symptom Stored")  
# EXTRACT JSON 
def extract_json(text): 
    try: 
        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        ) 
        if match: 
            return json.loads(
                match.group()
            ) 
    except Exception as e: 
        print(
            "[DEBUG] JSON Extraction Error:",
            e 
        ) 
    return None 
# LLM ANALYSIS 
def analyze_symptoms(symptom): 
    history = get_patient_context() 
    prompt = f"""
You are a medical assistant. 
Patient History:
{history} 
Current Symptoms:
{symptom} 
IMPORTANT: 
Return ONLY valid JSON. 
Do not use markdown. 
Do not use ```json. 
Do not provide explanations. 
Format: 
{{
    "possible_condition":"",
    "reason":"",
    "suggested_medicines":[]
}}
""" 
    response = llm.invoke(prompt) 
    return response.content  
# SAVE MEDICINE HISTORY 
def save_medicine_history(
        symptom,
        data): 
    history_record = { 
        "date":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ), 
        "symptom":
            symptom, 
        "possible_condition":
            data.get(
                "possible_condition",
                ""
            ), 
        "reason":
            data.get(
                "reason",
                ""
            ), 
        "suggested_medicines":
            data.get(
                "suggested_medicines",
                []
            )
    } 
    records[patient_name][
        "medicine_history"
    ].append(history_record) 
    save_records(records) 
    print(
        "[DEBUG] Medicine History Saved"
    )  
# MAIN 
print("\n" + "=" * 50)
print("AI MEDICAL AGENT")
print("=" * 50) 
symptom = input(
    "\nEnter Symptoms: "
).strip() 
# Store symptom 
save_symptom(symptom) 
print(
    "\n[DEBUG] Calling LLM..."
) 
result = analyze_symptoms(
    symptom
) 
print(
    "\n[DEBUG] Raw LLM Output:"
) 
print(result) 
data = extract_json(result) 
if data: 
    save_medicine_history(
        symptom,
        data
    ) 
    records[patient_name][
        "conversation"
    ].append(
        {
            "user": symptom,
            "assistant": data
        }
    ) 
    save_records(records) 
    print("\nAnalysis Result\n") 
    print(
        json.dumps(
            data,
            indent=4
        )
    ) 
else: 
    print(
        "\nFailed to parse JSON response."
    ) 
print(
    "\nProgram Finished."
)  

