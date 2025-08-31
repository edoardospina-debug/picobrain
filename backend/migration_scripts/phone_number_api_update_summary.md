# Phone Number Splitting - API Update Summary
## Date: 2025-08-30

## ✅ Completed Tasks

### 1. Updated Pydantic Schemas (`/backend/app/schemas/core.py`)

#### Person Schemas
**Changed fields:**
- Removed: `phone_mobile: str`
- Added:
  - `phone_mobile_country_code: Optional[str]` (max 6 chars)
  - `phone_mobile_number: Optional[str]` (max 20 chars)
  - `phone_home_country_code: Optional[str]` (max 6 chars)
  - `phone_home_number: Optional[str]` (max 20 chars)

**Additional fields added to match database:**
- `middle_name: Optional[str]`
- `nationality: Optional[str]` (2-char country code)
- `id_type: Optional[str]` (passport, national ID, etc.)
- `id_number: Optional[str]`
- `created_at: datetime`
- `updated_at: datetime`

#### Clinic Schemas
**Changed fields:**
- Removed: `phone: str`
- Added:
  - `phone_country_code: Optional[str]` (max 6 chars)
  - `phone_number: Optional[str]` (max 20 chars)

**Additional fields added to match database:**
- `address_line_1: Optional[str]`
- `address_line_2: Optional[str]`
- `state_province: Optional[str]`
- `postal_code: Optional[str]`
- `email: Optional[EmailStr]`
- `tax_id: Optional[str]`
- `created_at: datetime`
- `updated_at: datetime`
- `temp_id: Optional[int]` (migration helper)

#### Employee Schemas
**Additional fields added to match database:**
- `specialization: Optional[str]`
- `license_expiry: Optional[date]`
- `hire_date: date`
- `termination_date: Optional[date]`
- `base_salary_minor: Optional[int]` (stored in cents/pence)
- `salary_currency: Optional[str]`
- `commission_rate: Optional[Decimal]`
- `created_at: datetime`
- `updated_at: datetime`
- `temp_id: Optional[int]` (migration helper)

#### Client Schemas
**Additional fields added:**
- `acquisition_date: Optional[date]`
- `temp_id: Optional[int]` (migration helper)

#### New Utility Schemas
Added helper schemas for phone number handling:
```python
class PhoneNumber(BaseModel):
    country_code: str  # Pattern: ^\+\d{1,5}$
    number: str        # Pattern: ^\d{4,20}$
    
    @property
    def full_number(self) -> str:
        return f"{self.country_code} {self.number}"

class PhoneNumberUpdate(BaseModel):
    country_code: Optional[str]
    number: Optional[str]
```

### 2. Updated API Endpoints

#### `/api/v1/persons/` Endpoint Updates
**Enhanced validation:**
- Phone fields must be provided in pairs (country_code + number)
- If one is provided without the other, returns 400 error
- Validation applies to both CREATE and UPDATE operations

**New utility endpoints:**
- `POST /api/v1/persons/validate-phone` - Validate phone number format
- `GET /api/v1/persons/{person_id}/formatted-phones` - Get formatted phone numbers

**Updated documentation:**
- Added docstring explanations for split phone fields
- Clear error messages for validation failures

#### `/api/v1/clinics/` Endpoint Updates
**Enhanced validation:**
- Phone fields must be provided in pairs
- Email uniqueness validation
- Full address field support

**New utility endpoints:**
- `GET /api/v1/clinics/{clinic_id}/formatted-address` - Get full formatted address
- `GET /api/v1/clinics/{clinic_id}/contact-info` - Get structured contact information

### 3. Schema Module Exports Updated
Updated `/backend/app/schemas/__init__.py` to include:
- `UserRole` enum
- `PhoneNumber` utility schema
- `PhoneNumberUpdate` utility schema

## 📋 API Usage Examples

### Creating a Person with Split Phone Numbers
```json
POST /api/v1/persons/
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone_mobile_country_code": "+1",
  "phone_mobile_number": "5551234567",
  "phone_home_country_code": "+1",
  "phone_home_number": "5559876543",
  "gender": "M",
  "nationality": "US"
}
```

### Updating a Clinic with Split Phone
```json
PUT /api/v1/clinics/{clinic_id}
{
  "phone_country_code": "+44",
  "phone_number": "2071234567",
  "address_line_1": "123 Main Street",
  "city": "London",
  "country_code": "GB"
}
```

### Validation Error Examples
```json
// Missing phone number (only country code provided)
{
  "detail": "Both country code and number must be provided for mobile phone"
}

// Email already exists
{
  "detail": "Email already registered"
}
```

## 🔧 Technical Details

### Phone Number Storage Format
- **Country Code**: VARCHAR(6) - Stores '+1', '+44', '+351', etc.
- **Number**: VARCHAR(20) - Stores national number portion
- **Validation Pattern**: 
  - Country code: `^\+\d{1,5}$`
  - Number: `^\d{4,20}$`

### Backward Compatibility
- Old single phone field endpoints removed
- All existing API consumers must update to use split fields
- Migration helper fields (temp_id) excluded from normal operations

### Performance Considerations
- No additional database queries required
- Phone validation happens at API layer
- Formatted phone numbers computed on-demand

## ⚠️ Important Notes

1. **Database Migration Not Executed**: The database schema has been updated but data migration was not performed per your request

2. **Frontend Updates Required**: All forms and displays using phone fields need updates to handle split fields

3. **Validation Requirements**: Both parts of a phone number must be provided together or both must be null

4. **Testing Recommended**: All endpoints should be tested with the new field structure before production deployment

## 📝 Files Modified

1. `/backend/app/schemas/core.py` - Complete rewrite with all new fields
2. `/backend/app/api/v1/endpoints/persons.py` - Added phone validation and utility endpoints
3. `/backend/app/api/v1/endpoints/clinics.py` - Added address/contact utility endpoints
4. `/backend/app/schemas/__init__.py` - Updated exports
5. `/backend/phone_number_api_update_summary.md` - This summary document (new)

## Next Steps (Not Executed)

These are the remaining tasks that were NOT executed per your request:

1. ❌ **Data Migration**: Migrate existing phone data to split fields
2. ❌ **Frontend Updates**: Update all forms and displays
3. ❌ **Integration Testing**: Test all endpoints with new structure
4. ❌ **Documentation**: Update API documentation/OpenAPI specs
5. ❌ **Client Libraries**: Update any generated client libraries

---

All Pydantic schemas and API endpoints have been successfully updated to handle the split phone number fields. The API is ready to accept and return data in the new format.
