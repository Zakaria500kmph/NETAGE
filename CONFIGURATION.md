# Configuration Guide

## Database Configuration

The application uses the following database credentials by default:

- **Host**: `dpg-d2g31b75r7bs73eiedhg-a.oregon-postgres.render.com`
- **Port**: `5432`
- **Database**: `netage_testing`
- **Username**: `netage_testing_user`
- **Password**: `AxnL2z8PiJWfOn6YEmj4TxGum0qn37ry`

## Environment Variables

You can override the default configuration by setting environment variables. Create a `.env` file in the project root with the following variables:

```bash
# Database Configuration
DATABASE_HOST=dpg-d2g31b75r7bs73eiedhg-a.oregon-postgres.render.com
DATABASE_PORT=5432
DATABASE_NAME=netage_testing
DATABASE_USER=netage_testing_user
DATABASE_PASSWORD=AxnL2z8PiJWfOn6YEmj4TxGum0qn37ry

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000
SECRET_KEY=your-secret-key-here-change-in-production

# CORS Configuration
CORS_ORIGINS=*

# Logging Configuration
LOG_LEVEL=INFO
```

## Configuration File

The main configuration is handled in `config.py` which:

1. Loads environment variables from `.env` file if it exists
2. Provides default values for all settings
3. Constructs the database URL automatically
4. Provides helper methods for database configuration

## Usage

The configuration is automatically used throughout the application:

- **Database Connection**: Uses `settings.get_database_url()`
- **FastAPI App**: Uses `settings.API_TITLE`, `settings.API_DESCRIPTION`, etc.
- **Server Settings**: Uses `settings.HOST` and `settings.PORT`

## Security Notes

1. **Never commit the `.env` file** to version control
2. **Change the SECRET_KEY** in production
3. **Use environment variables** for sensitive data in production
4. **The current credentials are for testing** - use different ones for production

## Production Deployment

For production deployment:

1. Set all sensitive environment variables
2. Change the SECRET_KEY
3. Set DEBUG=False
4. Use proper CORS_ORIGINS (not "*")
5. Use a production database
