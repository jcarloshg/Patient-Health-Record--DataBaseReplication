
import time
import requests
import random
import uuid

# from concurrent.futures import ThreadPoolExecutor

url = "http://localhost:8000/patient-register"
total_requests = 1000
# concurrency = 10000  # How many at once

first_name_list = [
    "Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah",
    "Isaac", "Julia", "Kevin", "Laura", "Michael", "Nina", "Oscar", "Paula",
    "Quentin", "Rachel", "Samuel", "Tina", "Uma", "Victor", "Wendy", "Xavier",
    "Yara", "Zane", "Amber", "Brian", "Carmen", "Derek", "Elena", "Frank",
    "Grace", "Henry", "Ivy", "Jack", "Kara", "Liam", "Mona", "Noah"
]
last_name_list = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
]


def get_date_of_birth_random():
    """Generate a random date of birth between 1940-01-01 and 2020-12-31."""
    year = random.randint(1940, 2020)
    month = random.randint(1, 12)
    if month == 2:
        day = random.randint(1, 28)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:
        day = random.randint(1, 31)
    return f"{year:04d}-{month:02d}-{day:02d}"


def get_random_email(first_name, last_name):
    domains = ["example.com", "test.com", "mail.com", "demo.com"]
    return f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 1000)}@{random.choice(domains)}"


def get_random_phone_number():
    return f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"


address_list = [
    "123 Main St, Springfield",
    "456 Oak Ave, Rivertown",
    "789 Pine Rd, Lakeview",
    "101 Maple Dr, Hillcrest",
    "202 Elm St, Brookside",
    "303 Cedar Ln, Fairview",
    "404 Birch Blvd, Westfield",
    "505 Walnut St, Eastwood",
    "606 Chestnut Ave, Northgate",
    "707 Aspen Ct, Southport",
    "808 Willow Way, Greenfield",
    "909 Poplar Pl, Sunnydale",
    "111 Spruce St, Riverbend",
    "222 Sycamore Rd, Pleasantville",
    "333 Magnolia Ln, Woodridge",
    "444 Hickory Dr, Meadowbrook",
    "555 Redwood St, Parkside",
    "666 Dogwood Ave, Crestview",
    "777 Alder Ct, Lakeshore",
    "888 Cypress Pl, Highland",
    "999 Juniper St, Valleyview",
    "1212 Palm Ave, Rosewood",
    "1313 Olive Rd, Silverlake",
    "1414 Peach Ln, Maplewood",
    "1515 Plum Dr, Oakwood",
    "1616 Cherry St, Pinecrest",
    "1717 Apple Ave, Willowbrook",
    "1818 Lemon Ct, Cedarville",
    "1919 Lime Pl, Ashland",
    "2020 Orange St, Birchwood",
    "2121 Pear Ave, Elmwood",
    "2222 Fig Rd, Hawthorne",
    "2323 Grape Ln, Ironwood",
    "2424 Berry Dr, Juniper",
    "2525 Melon St, Kingswood",
    "2626 Kiwi Ave, Laurel",
    "2727 Mango Ct, Mulberry",
    "2828 Papaya Pl, Oakridge",
    "2929 Peach St, Pinehill",
    "3030 Nectarine Ave, Redwood"
]


def get_random_emergency_contact() -> str:
    first_name = random.choice(first_name_list)
    last_name = random.choice(last_name_list)
    return f"{first_name} {last_name}"


allergies = [
    "penicillin", "latex", "peanuts", "shellfish", "tree nuts", "milk", "eggs", "soy",
    "wheat", "fish", "bee stings", "pollen", "dust mites", "mold", "pet dander", "insect venom",
    "aspirin", "ibuprofen", "sulfa drugs", "nickel", "fragrances", "gluten", "sesame", "mustard",
    "celery", "lupin", "sunflower seeds", "strawberries", "tomatoes", "avocado", "banana", "kiwi",
    "chocolate", "corn", "garlic", "onion", "carrots", "apples", "chicken", "red meat"
]


def get_random_allergies() -> list:
    return random.sample(allergies, k=random.randint(0, 3))


medical_history = [
    "hypertension", "asthma", "diabetes", "coronary artery disease", "stroke", "chronic kidney disease",
    "COPD", "arthritis", "depression", "anxiety", "hyperlipidemia", "hypothyroidism", "migraine",
    "epilepsy", "cancer", "heart failure", "atrial fibrillation", "GERD", "peptic ulcer", "hepatitis",
    "HIV/AIDS", "tuberculosis", "anemia", "osteoporosis", "psoriasis", "eczema", "allergic rhinitis",
    "bipolar disorder", "schizophrenia", "obesity", "sleep apnea", "gout", "liver cirrhosis",
    "pancreatitis", "multiple sclerosis", "rheumatoid arthritis", "lupus", "Crohn's disease",
    "ulcerative colitis", "glaucoma", "cataract"
]


def get_random_medical_history() -> list:
    return random.sample(medical_history, k=random.randint(0, 2))


current_medications = [
    "lisinopril", "albuterol", "metformin", "atorvastatin", "amlodipine", "omeprazole",
    "simvastatin", "hydrochlorothiazide", "levothyroxine", "gabapentin", "losartan",
    "sertraline", "furosemide", "metoprolol", "pantoprazole", "prednisone",
    "clopidogrel", "amoxicillin", "azithromycin", "warfarin", "insulin", "tramadol",
    "fluoxetine", "citalopram", "montelukast", "spironolactone", "doxycycline",
    "tamsulosin", "rosuvastatin", "escitalopram", "pravastatin", "carvedilol",
    "duloxetine", "bupropion", "glipizide", "hydralazine", "cephalexin",
    "allopurinol", "enalapril", "buspirone", "meloxicam"
]


def get_random_current_medications() -> list:
    return random.sample(current_medications, k=random.randint(0, 3))


def register_patient(i):
    for intent in range(i):
        uuid_value = uuid.uuid4()
        first_name = random.choice(first_name_list)
        last_name = random.choice(last_name_list)
        data = {
            "uuid": str(uuid_value),
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": get_date_of_birth_random(),
            "email": get_random_email(first_name, last_name),
            "phone_number": get_random_phone_number(),
            "address": random.choice(address_list),
            "emergency_contact": get_random_emergency_contact(),
            "allergies": get_random_allergies(),
            "medical_history": get_random_medical_history(),
            "current_medications": get_random_current_medications()
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"Patient {intent} registered successfully.")
        else:
            print(
                f"Failed to register patient {intent}. Status code: {response.status_code}")
        # time.sleep(4)
    return


register_patient(total_requests)
