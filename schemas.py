from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import List, Optional

# Party Address Schemas
class PartyAddressBase(BaseModel):
    shipping_address: str
    country: str
    state: str
    district: Optional[str] = None
    city: Optional[str] = None
    zip_code: str
    is_primary: bool = True

class PartyAddressCreate(PartyAddressBase):
    pass

class PartyAddressResponse(PartyAddressBase):
    address_id: int
    party_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Contact Person Schemas
class ContactPersonBase(BaseModel):
    name: str
    mobile_number: str
    email_id: Optional[str] = None
    designation: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    address: Optional[str] = None
    aadhar_number: Optional[str] = None
    pan_number: Optional[str] = None
    is_primary: bool = True

class ContactPersonCreate(ContactPersonBase):
    pass

class ContactPersonResponse(ContactPersonBase):
    contact_id: int
    party_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Party Account Details Schemas
class PartyAccountDetailsBase(BaseModel):
    account_name: str
    account_type: str
    main_group: str
    group_name: str
    remarks: Optional[str] = None

class PartyAccountDetailsCreate(PartyAccountDetailsBase):
    pass

class PartyAccountDetailsResponse(PartyAccountDetailsBase):
    account_id: int
    party_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Bank Details Schemas
class BankDetailsBase(BaseModel):
    bank_name: str
    branch_name: str
    account_holder_name: str
    account_number: str
    confirm_account_number: str
    account_type: Optional[str] = None
    ifsc_code: str
    bank_address: Optional[str] = None
    is_primary: bool = True

class BankDetailsCreate(BankDetailsBase):
    pass

class BankDetailsResponse(BankDetailsBase):
    bank_id: int
    party_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Products Schemas
class ProductsBase(BaseModel):
    product_code: str
    product_name: str
    group_name: str
    sub_group: Optional[str] = None
    item: Optional[str] = None
    stock_keeping_unit: Optional[str] = None

class ProductsCreate(ProductsBase):
    pass

class ProductsResponse(ProductsBase):
    product_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Party Products Schemas
class PartyProductsBase(BaseModel):
    product_id: int
    quantity: Optional[int] = None

class PartyProductsCreate(PartyProductsBase):
    pass

class PartyProductsResponse(PartyProductsBase):
    party_product_id: int
    party_id: int
    created_at: datetime
    product: ProductsResponse
    
    class Config:
        from_attributes = True

# Payment Terms Schemas
class PaymentTermsBase(BaseModel):
    term_description: str
    payment_days: int
    cash_discount: Optional[float] = None
    variable_days: Optional[int] = None
    sms_days: Optional[int] = None
    is_default: bool = False

class PaymentTermsCreate(PaymentTermsBase):
    pass

class PaymentTermsResponse(PaymentTermsBase):
    term_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Party Payment Terms Schemas
class PartyPaymentTermsBase(BaseModel):
    term_id: int
    is_default: bool = False

class PartyPaymentTermsCreate(PartyPaymentTermsBase):
    pass

class PartyPaymentTermsResponse(PartyPaymentTermsBase):
    party_term_id: int
    party_id: int
    created_at: datetime
    payment_term: PaymentTermsResponse
    
    class Config:
        from_attributes = True

# Party Master Schemas
class PartyMasterBase(BaseModel):
    party_code: str
    party_name: str
    type_of_firm: str
    email_id: str
    mobile_number: str
    gst_number: Optional[str] = None
    fssai_number: Optional[str] = None
    pan_number: str
    tan_number: Optional[str] = None
    credit_limit: Optional[float] = None
    credit_days: Optional[int] = None
    udyam_aadhar_number: Optional[str] = None
    court_case_pending: bool = False
    billing_same_as_shipping: bool = False
    turnover_declaration_certificate: Optional[str] = None

class PartyMasterCreate(PartyMasterBase):
    addresses: Optional[List[PartyAddressCreate]] = []
    contact_persons: Optional[List[ContactPersonCreate]] = []
    account_details: Optional[PartyAccountDetailsCreate] = None
    bank_details: Optional[BankDetailsCreate] = None

class PartyMasterUpdate(BaseModel):
    party_name: Optional[str] = None
    type_of_firm: Optional[str] = None
    email_id: Optional[str] = None
    mobile_number: Optional[str] = None
    gst_number: Optional[str] = None
    fssai_number: Optional[str] = None
    pan_number: Optional[str] = None
    tan_number: Optional[str] = None
    credit_limit: Optional[float] = None
    credit_days: Optional[int] = None
    udyam_aadhar_number: Optional[str] = None
    court_case_pending: Optional[bool] = None
    billing_same_as_shipping: Optional[bool] = None
    turnover_declaration_certificate: Optional[str] = None

class PartyMasterResponse(PartyMasterBase):
    party_id: int
    created_at: datetime
    updated_at: datetime
    addresses: List[PartyAddressResponse] = []
    contact_persons: List[ContactPersonResponse] = []
    account_details: Optional[PartyAccountDetailsResponse] = None
    bank_details: Optional[BankDetailsResponse] = None
    
    class Config:
        from_attributes = True

class PartyMasterListResponse(BaseModel):
    party_id: int
    party_code: str
    party_name: str
    gst_number: Optional[str]
    fssai_number: Optional[str]
    contact_person: Optional[str]
    mobile_number: str
    location: Optional[str]
    
    class Config:
        from_attributes = True

# Master Types Schemas
class MasterTypesBase(BaseModel):
    type_name: str
    description: Optional[str] = None

class MasterTypesCreate(MasterTypesBase):
    pass

class MasterTypesResponse(MasterTypesBase):
    type_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Account Groups Schemas
class AccountGroupsBase(BaseModel):
    main_group: str
    group_name: str
    from_account_no: Optional[str] = None
    to_account_no: Optional[str] = None

class AccountGroupsCreate(AccountGroupsBase):
    pass

class AccountGroupsResponse(AccountGroupsBase):
    group_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
