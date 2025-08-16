# NETAGE BI - Party Master API

A complete FastAPI backend for the NETAGE BI Party Master management system, featuring comprehensive party management with all related entities like addresses, contact persons, account details, bank details, products, and payment terms.

## 🚀 Features

- **Complete Party Management** - Full CRUD operations for party master data
- **Multi-step Party Creation** - Support for all 5 steps: Details, Legal, Account, Products, Payment Terms
- **Address Management** - Multiple addresses per party with primary designation
- **Contact Person Management** - Multiple contact persons with detailed information
- **Account Details** - Financial account mapping and grouping
- **Bank Details** - Complete banking information with validation
- **Product Management** - Product catalog and party-product associations
- **Payment Terms** - Flexible payment terms with default settings
- **Master Data** - Support for master types and account groups
- **Search & Filter** - Advanced search capabilities
- **Auto-generated Documentation** - Interactive API docs with Swagger UI

## 📁 Project Structure

```
├── main.py              # FastAPI application with all routes
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic request/response schemas
├── init_db.py           # Database initialization script
├── test_api.py          # Comprehensive API testing suite
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🗄️ Database Schema

The system includes the following tables:

- **party_master** - Main party information
- **party_address** - Party addresses
- **contact_person** - Contact person details
- **party_account_details** - Account information
- **bank_details** - Banking information
- **products** - Product catalog
- **party_products** - Party-product associations
- **payment_terms** - Payment terms master
- **party_payment_terms** - Party-payment term associations
- **master_types** - Firm types and other master data
- **account_groups** - Account grouping information

## 🛠️ Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## 📦 Installation

### 1. Clone or download the project files

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL

Make sure PostgreSQL is installed and running on your system.

**Default connection details:**
- Host: `dpg-d2g31b75r7bs73eiedhg-a.oregon-postgres.render.com`
- Port: `5432`
- Username: `netage_testing_user`
- Password: `AxnL2z8PiJWfOn6YEmj4TxGum0qn37ry`
- Database: `netage_testing`

If you have different PostgreSQL credentials, create a `.env` file or set environment variables. See `CONFIGURATION.md` for details.

### 4. Initialize the database

```bash
python init_db.py
```

This script will:
- Test the database connection
- Create all tables with proper relationships
- Insert sample master data (firm types, account groups, payment terms, products)

## 🚀 Running the Application

### Start the FastAPI server

```bash
python main.py
```

The server will start on `http://localhost:8000`

### Alternative: Using uvicorn directly

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📚 API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

## 🔧 API Endpoints

### Health Check
- `GET /health` - Check if the API is running

### Party Management
- `POST /parties/` - Create a new party with all details
- `GET /parties/` - Get all parties (with search and pagination)
- `GET /parties/{party_id}` - Get a specific party with all related data
- `PUT /parties/{party_id}` - Update party information
- `DELETE /parties/{party_id}` - Delete a party

### Address Management
- `POST /parties/{party_id}/addresses/` - Add address to party
- `GET /parties/{party_id}/addresses/` - Get all addresses for a party

### Contact Person Management
- `POST /parties/{party_id}/contacts/` - Add contact person to party
- `GET /parties/{party_id}/contacts/` - Get all contact persons for a party

### Account Details
- `POST /parties/{party_id}/account-details/` - Add account details to party
- `GET /parties/{party_id}/account-details/` - Get account details for a party

### Bank Details
- `POST /parties/{party_id}/bank-details/` - Add bank details to party
- `GET /parties/{party_id}/bank-details/` - Get all bank details for a party

### Product Management
- `POST /products/` - Create a new product
- `GET /products/` - Get all products (with search)
- `POST /parties/{party_id}/products/` - Add product to party
- `GET /parties/{party_id}/products/` - Get all products for a party
- `DELETE /parties/{party_id}/products/{product_id}` - Remove product from party

### Payment Terms
- `POST /payment-terms/` - Create a new payment term
- `GET /payment-terms/` - Get all payment terms
- `POST /parties/{party_id}/payment-terms/` - Add payment term to party
- `GET /parties/{party_id}/payment-terms/` - Get all payment terms for a party

### Master Data
- `GET /master-types/` - Get all master types (firm types)
- `GET /account-groups/` - Get all account groups

## 🧪 Testing the API

Run the comprehensive test suite to verify everything is working:

```bash
python test_api.py
```

This will test:
- Party creation with all related data
- Party listing and search
- Party updates
- Address and contact person management
- Product and payment term associations
- All master data endpoints

## 📝 Example Usage

### Create a Complete Party

```bash
curl -X POST "http://localhost:8000/parties/" \
     -H "Content-Type: application/json" \
     -d '{
       "party_code": "SNET345",
       "party_name": "LALIT KIRANA (MOTALA)",
       "type_of_firm": "Sole Proprietorship",
       "email_id": "lalitkiranastore@gmail.com",
       "mobile_number": "868-333-4878",
       "gst_number": "24AABCU9603R1ZV",
       "fssai_number": "11518041000578",
       "pan_number": "ABCDE1234F",
       "credit_limit": 500000.00,
       "credit_days": 30,
       "addresses": [
         {
           "shipping_address": "201, Shree Sai Heights, Near Athwa Gate, Ring Road, Surat, Gujarat - 395001",
           "country": "India",
           "state": "Gujarat",
           "district": "Surat",
           "city": "Surat",
           "zip_code": "395001",
           "is_primary": true
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
           "is_primary": true
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
         "ifsc_code": "SBIN0001234",
         "is_primary": true
       }
     }'
```

### Get All Parties with Search

```bash
curl "http://localhost:8000/parties/?search=LALIT&limit=10"
```

### Add Product to Party

```bash
curl -X POST "http://localhost:8000/parties/1/products/" \
     -H "Content-Type: application/json" \
     -d '{
       "product_id": 1,
       "quantity": 25
     }'
```

### Add Payment Term to Party

```bash
curl -X POST "http://localhost:8000/parties/1/payment-terms/" \
     -H "Content-Type: application/json" \
     -d '{
       "term_id": 1,
       "is_default": true
     }'
```

## 🔍 Search and Filtering

The API supports advanced search and filtering:

- **Party Search**: Search by party name, code, or GST number
- **Product Search**: Search by product name or code
- **Pagination**: Control results with `skip` and `limit` parameters

## 🛡️ Data Validation

The API includes comprehensive data validation:

- **Required Fields**: All mandatory fields are validated
- **Data Types**: Proper type checking for all fields
- **Business Rules**: Account number matching, unique constraints
- **Relationship Validation**: Foreign key constraints and cascading deletes

## 🔧 Configuration

The application uses a centralized configuration system. See `CONFIGURATION.md` for detailed configuration options.

You can customize the application by:
- Creating a `.env` file with your settings
- Setting environment variables
- Modifying `config.py` for defaults

Key configuration options:
- Database connection settings
- Application host and port
- Debug mode
- CORS settings
- Logging level

## 🚨 Troubleshooting

### Database Connection Issues

1. **Wrong credentials**: Check your `.env` file or environment variables
2. **Database connection failed**: Verify the database is accessible
3. **Tables don't exist**: Run `python init_db.py`

### Import Errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port Already in Use

If port 8000 is already in use, change it:
```bash
uvicorn main:app --port 8001
```

## 🚀 Production Deployment

For production deployment:

1. **Change default credentials** in `models.py`
2. **Set environment variables** for sensitive data
3. **Enable HTTPS**
4. **Set up proper logging**
5. **Use a production WSGI server** like Gunicorn
6. **Configure database connection pooling**
7. **Set up monitoring and health checks**

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at http://localhost:8000/docs
- Review the test suite in `test_api.py` for usage examples
- Ensure PostgreSQL is running and accessible
