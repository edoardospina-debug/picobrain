# PicoBrain Permission Matrix

## User Roles
- **admin**: Full system access
- **manager**: Clinic management access  
- **staff**: General staff access
- **medical**: Medical staff (doctors, nurses)
- **finance**: Financial operations
- **readonly**: View-only access

## Permission Matrix

### Clinics Module
| Action | admin | manager | staff | medical | finance | readonly |
|--------|-------|---------|-------|---------|---------|----------|
| View List | ✅ | ✅ | 👁️ | 👁️ | 👁️ | 👁️ |
| View Details | ✅ | ✅ | 👁️ | 👁️ | 👁️ | 👁️ |
| Create | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Edit | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Delete | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Export Data | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Employees Module
| Action | admin | manager | staff | medical | finance | readonly |
|--------|-------|---------|-------|---------|---------|----------|
| View List | ✅ | ✅ | ✅ | ✅ | ✅ | 👁️ |
| View Details | ✅ | ✅ | ✅ | ❌ | ✅ | 👁️ |
| View Salary | ✅ | ✅ | 🔒 | 🔒 | ✅ | ❌ |
| Create | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Edit | ✅ | ✅ | 🔒 | 🔒 | ✅ | ❌ |
| Edit Salary | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Delete | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Export Data | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Clients Module
| Action | admin | manager | staff | medical | finance | readonly |
|--------|-------|---------|-------|---------|---------|----------|
| View List | ✅ | ✅ | ✅ | ✅ | ✅ | 👁️ |
| View Details | ✅ | ✅ | ✅ | ✅ | ✅ | 👁️ |
| View Medical Records | ✅ | ✅ | ✅ | ✅ | ✅ | 👁️ |
| View Financial Info | ✅ | ✅ | ✅ | ✅ | ✅ | 👁️ |
| Create | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Edit | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Edit Medical Records | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Edit Financial Info | ✅ | ✅ | ✅ | 👁️ | ✅ | ❌ |
| Delete | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Export Data | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Users Module
| Action | admin | manager | staff | medical | finance | readonly |
|--------|-------|---------|-------|---------|---------|----------|
| View List | ✅ | 👁️ | 👁️ | 👁️ | 👁️ | 👁️ |
| View Details | ✅ | 🔒 | 🔒 | 🔒 | 🔒 | ❌ |
| Create | ✅ | 🔒 | 🔒 | 🔒 | 🔒 | ❌ |
| Edit | ✅ | 🔒 | 🔒 | 🔒 | 🔒 | ❌ |
| Change Role | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Reset Password | ✅ | 🔒 | 🔒 | 🔒 | 🔒 | ❌ |
| Delete | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Export Data | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Reports Module
| Action | admin | manager | staff | medical | finance | readonly |
|--------|-------|---------|-------|---------|---------|----------|
| View Financial Reports | ✅ | ✅ | 👁️ | 🔒 | ✅ | 👁️ |
| View Medical Reports | ✅ | ✅ | ✅ | ✅ | ✅ | 👁️ |
| View Operational Reports | ✅ | ✅ | ✅ | 👁️ | ✅ | 👁️ |
| Create Reports | ✅ | ✅ | ✅ | ❌ | ✅ | 👁️ |
| Export Data | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### System Settings
| Action | admin | manager | staff | medical | finance | readonly |
|--------|-------|---------|-------|---------|---------|----------|
| View Settings | ✅ | 👁️ | 👁️ | 👁️ | 👁️ | 👁️ |
| Edit Settings | ✅ | ❌ | ❌ | ❌ | 👁️ | 👁️ |
| View Audit Logs | ✅ | 👁️ | 👁️ | 👁️ | 👁️ | 👁️ |
| Export Data | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Special Permissions

### Cross-Clinic Access
| Role | Can Access All Clinics | Only Assigned Clinic |
|------|------------------------|---------------------|
| admin | ✅ | - |
| manager | ✅ | - |
| staff | - | ✅ |
| medical | - | ✅ |
| finance | ✅ | - |
| readonly | ✅ | - |

### Data Visibility Rules
| Data Type | Who Can See |
|-----------|-------------|
| Employee Personal Info | admin, manager, finance, staff, doctor (self) |
| Employee Salary | admin, manager, finance, staff, doctor (self) |
| Client Medical History | admin, manager, finance, staff, doctor |
| Client Financial Data | admin, manager, finance, staff, doctor |
| Audit Logs | admin, manager, finance |

## Instructions for Filling

Please replace all `?` with either:
- ✅ = Yes, has permission
- ❌ = No, doesn't have permission
- 🔒 = Only for own records (self)
- 👁️ = View only, no edit
- 🏥 = Only for assigned clinic

## Additional Notes

Add any special business rules or exceptions here:

1. 
2. 
3. 

---
**Save this file as:** `/Users/edo/PyProjects/picobrain/permissions-matrix.md`
