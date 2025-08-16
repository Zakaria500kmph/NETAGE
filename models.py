from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Date, DECIMAL, Text, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

from config import settings

# Create SQLAlchemy engine
engine = create_engine(settings.get_database_url())

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Database Models
class PartyMaster(Base):
    __tablename__ = "party_master"
    
    party_id = Column(Integer, primary_key=True, index=True)
    party_code = Column(String(20), unique=True, nullable=False, index=True)
    party_name = Column(String(100), nullable=False)
    type_of_firm = Column(String(50), nullable=False)
    email_id = Column(String(100), nullable=False)
    mobile_number = Column(String(15), nullable=False)
    gst_number = Column(String(20))
    fssai_number = Column(String(20))
    pan_number = Column(String(20), nullable=False)
    tan_number = Column(String(20))
    credit_limit = Column(DECIMAL(15,2))
    credit_days = Column(Integer)
    udyam_aadhar_number = Column(String(20))
    court_case_pending = Column(Boolean, default=False)
    billing_same_as_shipping = Column(Boolean, default=False)
    turnover_declaration_certificate = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    addresses = relationship("PartyAddress", back_populates="party", cascade="all, delete-orphan")
    contact_persons = relationship("ContactPerson", back_populates="party", cascade="all, delete-orphan")
    account_details = relationship("PartyAccountDetails", back_populates="party", cascade="all, delete-orphan")
    bank_details = relationship("BankDetails", back_populates="party", cascade="all, delete-orphan")
    party_products = relationship("PartyProducts", back_populates="party", cascade="all, delete-orphan")
    party_payment_terms = relationship("PartyPaymentTerms", back_populates="party", cascade="all, delete-orphan")

class PartyAddress(Base):
    __tablename__ = "party_address"
    
    address_id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey("party_master.party_id"))
    shipping_address = Column(Text, nullable=False)
    country = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    district = Column(String(50))
    city = Column(String(50))
    zip_code = Column(String(20), nullable=False)
    is_primary = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    party = relationship("PartyMaster", back_populates="addresses")

class ContactPerson(Base):
    __tablename__ = "contact_person"
    
    contact_id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey("party_master.party_id"))
    name = Column(String(100), nullable=False)
    mobile_number = Column(String(15), nullable=False)
    email_id = Column(String(100))
    designation = Column(String(50))
    gender = Column(String(10))
    birth_date = Column(Date)
    address = Column(Text)
    aadhar_number = Column(String(20))
    pan_number = Column(String(20))
    is_primary = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    party = relationship("PartyMaster", back_populates="contact_persons")

class PartyAccountDetails(Base):
    __tablename__ = "party_account_details"
    
    account_id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey("party_master.party_id"))
    account_name = Column(String(100), nullable=False)
    account_type = Column(String(50), nullable=False)
    main_group = Column(String(50), nullable=False)
    group_name = Column(String(50), nullable=False)
    remarks = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    party = relationship("PartyMaster", back_populates="account_details")

class BankDetails(Base):
    __tablename__ = "bank_details"
    
    bank_id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey("party_master.party_id"))
    bank_name = Column(String(100), nullable=False)
    branch_name = Column(String(100), nullable=False)
    account_holder_name = Column(String(100), nullable=False)
    account_number = Column(String(30), nullable=False)
    confirm_account_number = Column(String(30), nullable=False)
    account_type = Column(String(30))
    ifsc_code = Column(String(20), nullable=False)
    bank_address = Column(Text)
    cancelled_cheque_image = Column(Text)  # Store as base64 or file path
    is_primary = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    party = relationship("PartyMaster", back_populates="bank_details")

class Products(Base):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(20), unique=True, nullable=False, index=True)
    product_name = Column(String(100), nullable=False)
    group_name = Column(String(50), nullable=False)
    sub_group = Column(String(50))
    item = Column(String(50))
    stock_keeping_unit = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    party_products = relationship("PartyProducts", back_populates="product")

class PartyProducts(Base):
    __tablename__ = "party_products"
    
    party_product_id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey("party_master.party_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    party = relationship("PartyMaster", back_populates="party_products")
    product = relationship("Products", back_populates="party_products")
    
    __table_args__ = (UniqueConstraint('party_id', 'product_id', name='unique_party_product'),)

class PaymentTerms(Base):
    __tablename__ = "payment_terms"
    
    term_id = Column(Integer, primary_key=True, index=True)
    term_description = Column(String(100), nullable=False)
    payment_days = Column(Integer, nullable=False)
    cash_discount = Column(DECIMAL(5,2))
    variable_days = Column(Integer)
    sms_days = Column(Integer)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    party_payment_terms = relationship("PartyPaymentTerms", back_populates="payment_term")

class PartyPaymentTerms(Base):
    __tablename__ = "party_payment_terms"
    
    party_term_id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey("party_master.party_id"))
    term_id = Column(Integer, ForeignKey("payment_terms.term_id"))
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    party = relationship("PartyMaster", back_populates="party_payment_terms")
    payment_term = relationship("PaymentTerms", back_populates="party_payment_terms")
    
    __table_args__ = (UniqueConstraint('party_id', 'term_id', name='unique_party_term'),)

class MasterTypes(Base):
    __tablename__ = "master_types"
    
    type_id = Column(Integer, primary_key=True, index=True)
    type_name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class AccountGroups(Base):
    __tablename__ = "account_groups"
    
    group_id = Column(Integer, primary_key=True, index=True)
    main_group = Column(String(50), nullable=False)
    group_name = Column(String(50), nullable=False)
    from_account_no = Column(String(20))
    to_account_no = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (UniqueConstraint('main_group', 'group_name', name='unique_main_group'),)
