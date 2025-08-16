from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os
from typing import List, Optional
import uuid

from models import Base, engine, PartyMaster, PartyAddress, ContactPerson, PartyAccountDetails, BankDetails, Products, PartyProducts, PaymentTerms, PartyPaymentTerms, MasterTypes, AccountGroups
from schemas import *

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

from config import settings

# FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Utility function to generate party code
def generate_party_code():
    return f"SNET{str(uuid.uuid4().int)[:6]}"

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to NETAGE BI Party Master API!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

# Party Master Routes
@app.post("/parties/", response_model=PartyMasterResponse)
async def create_party(party: PartyMasterCreate, db: Session = Depends(get_db)):
    # Check if party code already exists
    existing_party = db.query(PartyMaster).filter(PartyMaster.party_code == party.party_code).first()
    if existing_party:
        raise HTTPException(status_code=400, detail="Party code already exists")
    
    # Create party master
    db_party = PartyMaster(**party.dict(exclude={'addresses', 'contact_persons', 'account_details', 'bank_details'}))
    db.add(db_party)
    db.commit()
    db.refresh(db_party)
    
    # Create addresses
    for address_data in party.addresses:
        db_address = PartyAddress(**address_data.dict(), party_id=db_party.party_id)
        db.add(db_address)
    
    # Create contact persons
    for contact_data in party.contact_persons:
        db_contact = ContactPerson(**contact_data.dict(), party_id=db_party.party_id)
        db.add(db_contact)
    
    # Create account details
    if party.account_details:
        db_account = PartyAccountDetails(**party.account_details.dict(), party_id=db_party.party_id)
        db.add(db_account)
    
    # Create bank details
    if party.bank_details:
        db_bank = BankDetails(**party.bank_details.dict(), party_id=db_party.party_id)
        db.add(db_bank)
    
    db.commit()
    db.refresh(db_party)
    return db_party

@app.get("/parties/", response_model=List[PartyMasterListResponse])
async def get_parties(
    skip: int = 0, 
    limit: int = 10, 
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(PartyMaster)
    
    if search:
        query = query.filter(
            (PartyMaster.party_name.ilike(f"%{search}%")) |
            (PartyMaster.party_code.ilike(f"%{search}%")) |
            (PartyMaster.gst_number.ilike(f"%{search}%"))
        )
    
    parties = query.offset(skip).limit(limit).all()
    
    # Transform to list response format
    result = []
    for party in parties:
        # Get primary contact person
        primary_contact = db.query(ContactPerson).filter(
            ContactPerson.party_id == party.party_id,
            ContactPerson.is_primary == True
        ).first()
        
        # Get primary address for location
        primary_address = db.query(PartyAddress).filter(
            PartyAddress.party_id == party.party_id,
            PartyAddress.is_primary == True
        ).first()
        
        result.append(PartyMasterListResponse(
            party_id=party.party_id,
            party_code=party.party_code,
            party_name=party.party_name,
            gst_number=party.gst_number,
            fssai_number=party.fssai_number,
            contact_person=primary_contact.name if primary_contact else None,
            mobile_number=party.mobile_number,
            location=primary_address.city if primary_address else None
        ))
    
    return result

@app.get("/parties/{party_id}", response_model=PartyMasterResponse)
async def get_party(party_id: int, db: Session = Depends(get_db)):
    party = db.query(PartyMaster).filter(PartyMaster.party_id == party_id).first()
    if party is None:
        raise HTTPException(status_code=404, detail="Party not found")
    return party

@app.put("/parties/{party_id}", response_model=PartyMasterResponse)
async def update_party(party_id: int, party_update: PartyMasterUpdate, db: Session = Depends(get_db)):
    db_party = db.query(PartyMaster).filter(PartyMaster.party_id == party_id).first()
    if db_party is None:
        raise HTTPException(status_code=404, detail="Party not found")
    
    # Update only provided fields
    update_data = party_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_party, field, value)
    
    db_party.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_party)
    return db_party

@app.delete("/parties/{party_id}")
async def delete_party(party_id: int, db: Session = Depends(get_db)):
    db_party = db.query(PartyMaster).filter(PartyMaster.party_id == party_id).first()
    if db_party is None:
        raise HTTPException(status_code=404, detail="Party not found")
    
    db.delete(db_party)
    db.commit()
    return {"message": "Party deleted successfully"}

# Address Routes
@app.post("/parties/{party_id}/addresses/", response_model=PartyAddressResponse)
async def create_party_address(
    party_id: int, 
    address: PartyAddressCreate, 
    db: Session = Depends(get_db)
):
    # Check if party exists
    party = db.query(PartyMaster).filter(PartyMaster.party_id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    
    db_address = PartyAddress(**address.dict(), party_id=party_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@app.get("/parties/{party_id}/addresses/", response_model=List[PartyAddressResponse])
async def get_party_addresses(party_id: int, db: Session = Depends(get_db)):
    addresses = db.query(PartyAddress).filter(PartyAddress.party_id == party_id).all()
    return addresses

# Contact Person Routes
@app.post("/parties/{party_id}/contacts/", response_model=ContactPersonResponse)
async def create_contact_person(
    party_id: int, 
    contact: ContactPersonCreate, 
    db: Session = Depends(get_db)
):
    # Check if party exists
    party = db.query(PartyMaster).filter(PartyMaster.party_id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    
    db_contact = ContactPerson(**contact.dict(), party_id=party_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/parties/{party_id}/contacts/", response_model=List[ContactPersonResponse])
async def get_contact_persons(party_id: int, db: Session = Depends(get_db)):
    contacts = db.query(ContactPerson).filter(ContactPerson.party_id == party_id).all()
    return contacts

# Account Details Routes
@app.post("/parties/{party_id}/account-details/", response_model=PartyAccountDetailsResponse)
async def create_account_details(
    party_id: int, 
    account: PartyAccountDetailsCreate, 
    db: Session = Depends(get_db)
):
    # Check if party exists
    party = db.query(PartyMaster).filter(PartyMaster.party_id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    
    # Check if account details already exist
    existing_account = db.query(PartyAccountDetails).filter(
        PartyAccountDetails.party_id == party_id
    ).first()
    if existing_account:
        raise HTTPException(status_code=400, detail="Account details already exist for this party")
    
    db_account = PartyAccountDetails(**account.dict(), party_id=party_id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@app.get("/parties/{party_id}/account-details/", response_model=PartyAccountDetailsResponse)
async def get_account_details(party_id: int, db: Session = Depends(get_db)):
    account = db.query(PartyAccountDetails).filter(PartyAccountDetails.party_id == party_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account details not found")
    return account

# Bank Details Routes
@app.post("/parties/{party_id}/bank-details/", response_model=BankDetailsResponse)
async def create_bank_details(
    party_id: int, 
    bank: BankDetailsCreate, 
    db: Session = Depends(get_db)
):
    # Check if party exists
    party = db.query(PartyMaster).filter(PartyMaster.party_id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    
    # Validate account numbers match
    if bank.account_number != bank.confirm_account_number:
        raise HTTPException(status_code=400, detail="Account numbers do not match")
    
    db_bank = BankDetails(**bank.dict(), party_id=party_id)
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank

@app.get("/parties/{party_id}/bank-details/", response_model=List[BankDetailsResponse])
async def get_bank_details(party_id: int, db: Session = Depends(get_db)):
    bank_details = db.query(BankDetails).filter(BankDetails.party_id == party_id).all()
    return bank_details

# Products Routes
@app.post("/products/", response_model=ProductsResponse)
async def create_product(product: ProductsCreate, db: Session = Depends(get_db)):
    # Check if product code already exists
    existing_product = db.query(Products).filter(Products.product_code == product.product_code).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product code already exists")
    
    db_product = Products(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[ProductsResponse])
async def get_products(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Products)
    
    if search:
        query = query.filter(
            (Products.product_name.ilike(f"%{search}%")) |
            (Products.product_code.ilike(f"%{search}%"))
        )
    
    products = query.offset(skip).limit(limit).all()
    return products

# Party Products Routes
@app.post("/parties/{party_id}/products/", response_model=PartyProductsResponse)
async def add_party_product(
    party_id: int, 
    party_product: PartyProductsCreate, 
    db: Session = Depends(get_db)
):
    # Check if party exists
    party = db.query(PartyMaster).filter(PartyMaster.party_id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    
    # Check if product exists
    product = db.query(Products).filter(Products.product_id == party_product.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if product already assigned to party
    existing = db.query(PartyProducts).filter(
        PartyProducts.party_id == party_id,
        PartyProducts.product_id == party_product.product_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already assigned to party")
    
    db_party_product = PartyProducts(**party_product.dict(), party_id=party_id)
    db.add(db_party_product)
    db.commit()
    db.refresh(db_party_product)
    return db_party_product

@app.get("/parties/{party_id}/products/", response_model=List[PartyProductsResponse])
async def get_party_products(party_id: int, db: Session = Depends(get_db)):
    party_products = db.query(PartyProducts).filter(PartyProducts.party_id == party_id).all()
    return party_products

@app.delete("/parties/{party_id}/products/{product_id}")
async def remove_party_product(party_id: int, product_id: int, db: Session = Depends(get_db)):
    party_product = db.query(PartyProducts).filter(
        PartyProducts.party_id == party_id,
        PartyProducts.product_id == product_id
    ).first()
    if not party_product:
        raise HTTPException(status_code=404, detail="Party product not found")
    
    db.delete(party_product)
    db.commit()
    return {"message": "Product removed from party successfully"}

# Payment Terms Routes
@app.post("/payment-terms/", response_model=PaymentTermsResponse)
async def create_payment_term(term: PaymentTermsCreate, db: Session = Depends(get_db)):
    db_term = PaymentTerms(**term.dict())
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term

@app.get("/payment-terms/", response_model=List[PaymentTermsResponse])
async def get_payment_terms(db: Session = Depends(get_db)):
    terms = db.query(PaymentTerms).all()
    return terms

# Party Payment Terms Routes
@app.post("/parties/{party_id}/payment-terms/", response_model=PartyPaymentTermsResponse)
async def add_party_payment_term(
    party_id: int, 
    party_term: PartyPaymentTermsCreate, 
    db: Session = Depends(get_db)
):
    # Check if party exists
    party = db.query(PartyMaster).filter(PartyMaster.party_id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    
    # Check if payment term exists
    payment_term = db.query(PaymentTerms).filter(PaymentTerms.term_id == party_term.term_id).first()
    if not payment_term:
        raise HTTPException(status_code=404, detail="Payment term not found")
    
    # Check if term already assigned to party
    existing = db.query(PartyPaymentTerms).filter(
        PartyPaymentTerms.party_id == party_id,
        PartyPaymentTerms.term_id == party_term.term_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Payment term already assigned to party")
    
    db_party_term = PartyPaymentTerms(**party_term.dict(), party_id=party_id)
    db.add(db_party_term)
    db.commit()
    db.refresh(db_party_term)
    return db_party_term

@app.get("/parties/{party_id}/payment-terms/", response_model=List[PartyPaymentTermsResponse])
async def get_party_payment_terms(party_id: int, db: Session = Depends(get_db)):
    party_terms = db.query(PartyPaymentTerms).filter(PartyPaymentTerms.party_id == party_id).all()
    return party_terms

# Account Groups Routes
@app.get("/account-groups/")
async def get_account_groups(db: Session = Depends(get_db)):
    groups = db.query(AccountGroups).all()
    return groups

# Master Types Routes
@app.get("/master-types/")
async def get_master_types(db: Session = Depends(get_db)):
    types = db.query(MasterTypes).all()
    return types

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
