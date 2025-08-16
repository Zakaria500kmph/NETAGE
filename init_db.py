import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import sys

from config import settings

# Database configuration
DATABASE_URL = settings.get_database_url()

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not to a specific database)
        db_config = settings.get_database_config()
        conn = psycopg2.connect(
            host=db_config["host"],
            port=db_config["port"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]  # Connect directly to the target database
        )
        cursor = conn.cursor()
        
        # Test the connection to the database
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Connected to PostgreSQL: {version[0]}")
        print(f"Database '{settings.DATABASE_NAME}' is accessible!")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
        sys.exit(1)



def create_tables():
    """Create all tables using SQLAlchemy"""
    try:
        from models import Base, engine
        Base.metadata.create_all(bind=engine)
        print("All tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def insert_sample_data():
    """Insert sample data for testing"""
    try:
        from models import SessionLocal, MasterTypes, AccountGroups, PaymentTerms, Products
        from datetime import datetime
        
        db = SessionLocal()
        
        # Insert master types
        master_types = [
            {"type_name": "Sole Proprietorship", "description": "Individual business ownership"},
            {"type_name": "Partnership", "description": "Business owned by two or more partners"},
            {"type_name": "Limited Liability Partnership (LLP)", "description": "Limited liability partnership"},
            {"type_name": "Private Limited Company", "description": "Private limited company"},
            {"type_name": "Public Limited Company", "description": "Public limited company"},
        ]
        
        for mt_data in master_types:
            existing = db.query(MasterTypes).filter(MasterTypes.type_name == mt_data["type_name"]).first()
            if not existing:
                mt = MasterTypes(**mt_data)
                db.add(mt)
        
        # Insert account groups
        account_groups = [
            {"main_group": "Cash & Cash Equivalents", "group_name": "Current Assets", "from_account_no": "100100000", "to_account_no": "100199999"},
            {"main_group": "Current Assets, Loans & Adv.", "group_name": "Current Assets", "from_account_no": "100200000", "to_account_no": "100299999"},
            {"main_group": "Inventories", "group_name": "Current Assets", "from_account_no": "100300000", "to_account_no": "100399999"},
            {"main_group": "Other Current Assets", "group_name": "Current Assets", "from_account_no": "100400000", "to_account_no": "100499999"},
            {"main_group": "Prepaid Expenses", "group_name": "Current Assets", "from_account_no": "100500000", "to_account_no": "100599999"},
            {"main_group": "Short Term Loan & Advances", "group_name": "Current Assets", "from_account_no": "100600000", "to_account_no": "100699999"},
            {"main_group": "Trade Receivables (Debtors)", "group_name": "Current Assets", "from_account_no": "100700000", "to_account_no": "100799999"},
            {"main_group": "Short Term Investments", "group_name": "Current Assets", "from_account_no": "100800000", "to_account_no": "100899999"},
        ]
        
        for ag_data in account_groups:
            existing = db.query(AccountGroups).filter(
                AccountGroups.main_group == ag_data["main_group"],
                AccountGroups.group_name == ag_data["group_name"]
            ).first()
            if not existing:
                ag = AccountGroups(**ag_data)
                db.add(ag)
        
        # Insert payment terms
        payment_terms = [
            {"term_description": "CASH DISCOUNT 0.5% (SAME DAY)", "payment_days": 2, "cash_discount": 0.5, "variable_days": 3, "sms_days": 1, "is_default": True},
            {"term_description": "PAYMENT IN 8 DAYS", "payment_days": 8, "cash_discount": 0.2, "variable_days": 5, "sms_days": 6, "is_default": False},
            {"term_description": "SECOND DAY 0.7% BILL DISCOUNT", "payment_days": 3, "cash_discount": 2.0, "variable_days": 21, "sms_days": 2, "is_default": False},
            {"term_description": "CASH DISCOUNT 4.5% (7 DAYS)", "payment_days": 7, "cash_discount": 3.0, "variable_days": 7, "sms_days": 5, "is_default": False},
        ]
        
        for pt_data in payment_terms:
            existing = db.query(PaymentTerms).filter(PaymentTerms.term_description == pt_data["term_description"]).first()
            if not existing:
                pt = PaymentTerms(**pt_data)
                db.add(pt)
        
        # Insert sample products
        products = [
            {"product_code": "703", "product_name": "CATTEL FEED 45 KG FULL TANK", "group_name": "CHANA", "sub_group": "CHANA", "item": "BESAN SINGLE", "stock_keeping_unit": "45 KG"},
            {"product_code": "382", "product_name": "RICE FLOUR 25KG BELPAN", "group_name": "CHANA", "sub_group": "CHANA", "item": "BESAN SINGLE", "stock_keeping_unit": "25 KG"},
            {"product_code": "624", "product_name": "WHEAT GERM RAW 25KG BELPAN", "group_name": "CHANA", "sub_group": "CHANA", "item": "BESAN SINGLE", "stock_keeping_unit": "25 KG"},
            {"product_code": "RM001", "product_name": "RM WHEAT LOKWAN", "group_name": "CHANA", "sub_group": "CHANA", "item": "BESAN SINGLE", "stock_keeping_unit": "25 KG"},
        ]
        
        for p_data in products:
            existing = db.query(Products).filter(Products.product_code == p_data["product_code"]).first()
            if not existing:
                p = Products(**p_data)
                db.add(p)
        
        db.commit()
        print("Sample data inserted successfully!")
        db.close()
        return True
        
    except Exception as e:
        print(f"Error inserting sample data: {e}")
        return False

if __name__ == "__main__":
    print("Setting up NETAGE BI PostgreSQL database...")
    print("=" * 60)
    
    # Step 1: Test database connection
    try:
        create_database()
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your database credentials and ensure the database exists.")
        sys.exit(1)
    
    # Step 2: Create tables
    if create_tables():
        print("✅ Tables created successfully!")
        
        # Step 3: Insert sample data
        if insert_sample_data():
            print("✅ Sample data inserted successfully!")
        else:
            print("⚠️ Sample data insertion failed!")
    else:
        print("❌ Table creation failed!")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Database setup completed!")
    print("You can now run the FastAPI application with: python main.py")
    print("API Documentation will be available at: http://localhost:8000/docs")
