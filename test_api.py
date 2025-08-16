import requests
import json
from datetime import datetime, date

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running.")

def test_create_party():
    """Test creating a party with all details"""
    print("\nTesting party creation...")
    party_data = {
        "party_code": "SNET345",
        "party_name": "LALIT KIRANA (MOTALA)",
        "type_of_firm": "Sole Proprietorship",
        "email_id": "lalitkiranastore@gmail.com",
        "mobile_number": "868-333-4878",
        "gst_number": "24AABCU9603R1ZV",
        "fssai_number": "11518041000578",
        "pan_number": "ABCDE1234F",
        "tan_number": None,
        "credit_limit": 500000.00,
        "credit_days": 30,
        "udyam_aadhar_number": None,
        "court_case_pending": False,
        "billing_same_as_shipping": False,
        "turnover_declaration_certificate": None,
        "addresses": [
            {
                "shipping_address": "201, Shree Sai Heights, Near Athwa Gate, Ring Road, Surat, Gujarat - 395001",
                "country": "India",
                "state": "Gujarat",
                "district": "Surat",
                "city": "Surat",
                "zip_code": "395001",
                "is_primary": True
            }
        ],
        "contact_persons": [
            {
                "name": "Rajesh Sharma",
                "mobile_number": "888-333-4878",
                "email_id": "lalitkiranastore@gmail.com",
                "designation": "Sales Manager",
                "gender": "Male",
                "birth_date": "1990-06-12",
                "address": "101, Green Park Society, Adajan, Surat, Gujarat - 395009",
                "aadhar_number": None,
                "pan_number": None,
                "is_primary": True
            }
        ],
        "account_details": {
            "account_name": "S MAHABOOB BASHA (CHAGALAMARI)",
            "account_type": "Transport",
            "main_group": "Cash & Cash Equivalents",
            "group_name": "Current Assets",
            "remarks": "Regular Inventories required."
        },
        "bank_details": {
            "bank_name": "State Bank of India",
            "branch_name": "Ring Road Branch",
            "account_holder_name": "Vikram Shah",
            "account_number": "123456789012",
            "confirm_account_number": "123456789012",
            "account_type": "Savings",
            "ifsc_code": "SBIN0001234",
            "bank_address": "15, Ring Road, Surat, Gujarat - 395001",
            "is_primary": True
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/parties/", json=party_data)
        if response.status_code == 200:
            print("✅ Party created successfully")
            party = response.json()
            print(f"Created party ID: {party['party_id']}")
            return party["party_id"]
        else:
            print(f"❌ Party creation failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")
        return None

def test_get_parties():
    """Test getting all parties"""
    print("\nTesting get all parties...")
    try:
        response = requests.get(f"{BASE_URL}/parties/")
        if response.status_code == 200:
            parties = response.json()
            print(f"✅ Retrieved {len(parties)} parties")
            for party in parties:
                print(f"  - {party['party_code']}: {party['party_name']} ({party['mobile_number']})")
        else:
            print(f"❌ Get parties failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def test_get_party(party_id):
    """Test getting a specific party"""
    print(f"\nTesting get party {party_id}...")
    try:
        response = requests.get(f"{BASE_URL}/parties/{party_id}")
        if response.status_code == 200:
            party = response.json()
            print("✅ Party retrieved successfully")
            print(f"Party: {party['party_name']} ({party['party_code']})")
            print(f"Addresses: {len(party['addresses'])}")
            print(f"Contact Persons: {len(party['contact_persons'])}")
        else:
            print(f"❌ Get party failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def test_update_party(party_id):
    """Test updating a party"""
    print(f"\nTesting update party {party_id}...")
    update_data = {
        "credit_limit": 750000.00,
        "credit_days": 45,
        "court_case_pending": True
    }
    
    try:
        response = requests.put(f"{BASE_URL}/parties/{party_id}", json=update_data)
        if response.status_code == 200:
            party = response.json()
            print("✅ Party updated successfully")
            print(f"Updated credit limit: {party['credit_limit']}")
            print(f"Updated credit days: {party['credit_days']}")
        else:
            print(f"❌ Update party failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def test_add_party_address(party_id):
    """Test adding an address to a party"""
    print(f"\nTesting add address to party {party_id}...")
    address_data = {
        "shipping_address": "301, Business Park, Near Railway Station, Mumbai, Maharashtra - 400001",
        "country": "India",
        "state": "Maharashtra",
        "district": "Mumbai",
        "city": "Mumbai",
        "zip_code": "400001",
        "is_primary": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/parties/{party_id}/addresses/", json=address_data)
        if response.status_code == 200:
            address = response.json()
            print("✅ Address added successfully")
            print(f"Address ID: {address['address_id']}")
        else:
            print(f"❌ Add address failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def test_add_contact_person(party_id):
    """Test adding a contact person to a party"""
    print(f"\nTesting add contact person to party {party_id}...")
    contact_data = {
        "name": "Priya Patel",
        "mobile_number": "987-654-3210",
        "email_id": "priya.patel@example.com",
        "designation": "Accounts Manager",
        "gender": "Female",
        "birth_date": "1985-03-15",
        "address": "202, Sunshine Apartments, Bandra West, Mumbai - 400050",
        "aadhar_number": None,
        "pan_number": None,
        "is_primary": False
    }
    
    try:
        response = requests.post(f"{BASE_URL}/parties/{party_id}/contacts/", json=contact_data)
        if response.status_code == 200:
            contact = response.json()
            print("✅ Contact person added successfully")
            print(f"Contact ID: {contact['contact_id']}")
        else:
            print(f"❌ Add contact person failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def test_get_products():
    """Test getting all products"""
    print("\nTesting get all products...")
    try:
        response = requests.get(f"{BASE_URL}/products/")
        if response.status_code == 200:
            products = response.json()
            print(f"✅ Retrieved {len(products)} products")
            for product in products:
                print(f"  - {product['product_code']}: {product['product_name']}")
        else:
            print(f"❌ Get products failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def test_add_party_product(party_id):
    """Test adding a product to a party"""
    print(f"\nTesting add product to party {party_id}...")
    
    # First get available products
    try:
        products_response = requests.get(f"{BASE_URL}/products/")
        if products_response.status_code == 200:
            products = products_response.json()
            if products:
                product_id = products[0]['product_id']
                party_product_data = {
                    "product_id": product_id,
                    "quantity": 25
                }
                
                response = requests.post(f"{BASE_URL}/parties/{party_id}/products/", json=party_product_data)
                if response.status_code == 200:
                    party_product = response.json()
                    print("✅ Product added to party successfully")
                    print(f"Party Product ID: {party_product['party_product_id']}")
                else:
                    print(f"❌ Add product to party failed: {response.status_code}")
            else:
                print("⚠️ No products available to add")
        else:
            print(f"❌ Get products failed: {products_response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def test_get_payment_terms():
    """Test getting all payment terms"""
    print("\nTesting get all payment terms...")
    try:
        response = requests.get(f"{BASE_URL}/payment-terms/")
        if response.status_code == 200:
            terms = response.json()
            print(f"✅ Retrieved {len(terms)} payment terms")
            for term in terms:
                print(f"  - {term['term_description']} ({term['payment_days']} days)")
        else:
            print(f"❌ Get payment terms failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def test_add_party_payment_term(party_id):
    """Test adding a payment term to a party"""
    print(f"\nTesting add payment term to party {party_id}...")
    
    # First get available payment terms
    try:
        terms_response = requests.get(f"{BASE_URL}/payment-terms/")
        if terms_response.status_code == 200:
            terms = terms_response.json()
            if terms:
                term_id = terms[0]['term_id']
                party_term_data = {
                    "term_id": term_id,
                    "is_default": True
                }
                
                response = requests.post(f"{BASE_URL}/parties/{party_id}/payment-terms/", json=party_term_data)
                if response.status_code == 200:
                    party_term = response.json()
                    print("✅ Payment term added to party successfully")
                    print(f"Party Term ID: {party_term['party_term_id']}")
                else:
                    print(f"❌ Add payment term to party failed: {response.status_code}")
            else:
                print("⚠️ No payment terms available to add")
        else:
            print(f"❌ Get payment terms failed: {terms_response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def test_get_master_types():
    """Test getting master types"""
    print("\nTesting get master types...")
    try:
        response = requests.get(f"{BASE_URL}/master-types/")
        if response.status_code == 200:
            types = response.json()
            print(f"✅ Retrieved {len(types)} master types")
            for type_item in types:
                print(f"  - {type_item['type_name']}")
        else:
            print(f"❌ Get master types failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def test_get_account_groups():
    """Test getting account groups"""
    print("\nTesting get account groups...")
    try:
        response = requests.get(f"{BASE_URL}/account-groups/")
        if response.status_code == 200:
            groups = response.json()
            print(f"✅ Retrieved {len(groups)} account groups")
            for group in groups:
                print(f"  - {group['main_group']} > {group['group_name']}")
        else:
            print(f"❌ Get account groups failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def test_search_parties():
    """Test searching parties"""
    print("\nTesting search parties...")
    try:
        response = requests.get(f"{BASE_URL}/parties/?search=LALIT")
        if response.status_code == 200:
            parties = response.json()
            print(f"✅ Search returned {len(parties)} parties")
            for party in parties:
                print(f"  - {party['party_name']} ({party['party_code']})")
        else:
            print(f"❌ Search parties failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")

def main():
    print("🚀 Starting NETAGE BI Party Master API Test Suite")
    print("=" * 70)
    
    # Test health check
    test_health_check()
    
    # Test party operations
    party_id = test_create_party()
    
    if party_id:
        test_get_parties()
        test_get_party(party_id)
        test_update_party(party_id)
        test_add_party_address(party_id)
        test_add_contact_person(party_id)
        test_search_parties()
    
    # Test product operations
    test_get_products()
    if party_id:
        test_add_party_product(party_id)
    
    # Test payment terms operations
    test_get_payment_terms()
    if party_id:
        test_add_party_payment_term(party_id)
    
    # Test master data
    test_get_master_types()
    test_get_account_groups()
    
    print("\n" + "=" * 70)
    print("🏁 Test suite completed!")
    print("\n📚 API Documentation available at:")
    print("   - Swagger UI: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")

if __name__ == "__main__":
    main()
