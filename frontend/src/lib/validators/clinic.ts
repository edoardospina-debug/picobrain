import { z } from 'zod';

// Currency codes (commonly used in medical practices)
export const CURRENCY_CODES = [
  'USD', 'EUR', 'GBP', 'CAD', 'AUD', 'NZD', 'JPY', 'CNY', 'INR', 'MXN', 'BRL'
] as const;

// Country codes (ISO 3166-1 alpha-2)
export const COUNTRY_CODES = [
  'US', 'CA', 'GB', 'FR', 'DE', 'IT', 'ES', 'AU', 'NZ', 'JP', 'CN', 'IN', 'MX', 'BR'
] as const;

// Phone validation regex
const PHONE_REGEX = /^[0-9\s\-\(\)]+$/;

// Email validation
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Clinic validation schema
export const clinicSchema = z.object({
  // Required fields
  code: z
    .string()
    .min(2, 'Code must be at least 2 characters')
    .max(20, 'Code must be at most 20 characters')
    .regex(/^[A-Z0-9_-]+$/i, 'Code can only contain letters, numbers, hyphens, and underscores')
    .transform((val) => val.toUpperCase()),
  
  name: z
    .string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must be at most 100 characters')
    .trim(),
  
  functional_currency: z
    .enum(CURRENCY_CODES, {
      errorMap: () => ({ message: 'Please select a valid currency' }),
    }),
  
  // Optional address fields
  address_line_1: z
    .string()
    .max(100, 'Address line 1 must be at most 100 characters')
    .optional()
    .nullable()
    .transform((val) => val?.trim() || null),
  
  address_line_2: z
    .string()
    .max(100, 'Address line 2 must be at most 100 characters')
    .optional()
    .nullable()
    .transform((val) => val?.trim() || null),
  
  city: z
    .string()
    .max(50, 'City must be at most 50 characters')
    .optional()
    .nullable()
    .transform((val) => val?.trim() || null),
  
  state_province: z
    .string()
    .max(50, 'State/Province must be at most 50 characters')
    .optional()
    .nullable()
    .transform((val) => val?.trim() || null),
  
  postal_code: z
    .string()
    .max(20, 'Postal code must be at most 20 characters')
    .optional()
    .nullable()
    .transform((val) => val?.trim() || null),
  
  country_code: z
    .enum(COUNTRY_CODES, {
      errorMap: () => ({ message: 'Please select a valid country' }),
    })
    .optional()
    .nullable(),
  
  // Contact fields
  phone_country_code: z
    .string()
    .regex(/^\d{1,4}$/, 'Phone country code must be 1-4 digits')
    .optional()
    .nullable()
    .transform((val) => val?.trim() || null),
  
  phone_number: z
    .string()
    .regex(PHONE_REGEX, 'Please enter a valid phone number')
    .max(20, 'Phone number must be at most 20 characters')
    .optional()
    .nullable()
    .transform((val) => val?.trim() || null),
  
  email: z
    .string()
    .regex(EMAIL_REGEX, 'Please enter a valid email address')
    .max(100, 'Email must be at most 100 characters')
    .optional()
    .nullable()
    .transform((val) => val?.trim()?.toLowerCase() || null),
  
  // Business fields
  tax_id: z
    .string()
    .max(50, 'Tax ID must be at most 50 characters')
    .optional()
    .nullable()
    .transform((val) => val?.trim() || null),
  
  is_active: z.boolean().default(true),
});

// Create request schema (for new clinics)
export const clinicCreateSchema = clinicSchema;

// Update request schema (all fields optional except id)
export const clinicUpdateSchema = clinicSchema.partial();

// Validation helpers
export const validateClinicCode = async (code: string, excludeId?: string): Promise<boolean> => {
  // This would call the API to check uniqueness
  // For now, return true
  return true;
};

// Custom refinements for form validation
export const clinicFormSchema = clinicSchema
  .refine(
    (data) => {
      // If phone number is provided, country code should also be provided
      if (data.phone_number && !data.phone_country_code) {
        return false;
      }
      return true;
    },
    {
      message: 'Phone country code is required when phone number is provided',
      path: ['phone_country_code'],
    }
  )
  .refine(
    (data) => {
      // If any address field is provided, at least city and country should be provided
      const hasAnyAddress = data.address_line_1 || data.address_line_2 || data.postal_code || data.state_province;
      if (hasAnyAddress && (!data.city || !data.country_code)) {
        return false;
      }
      return true;
    },
    {
      message: 'City and country are required when providing address details',
      path: ['city'],
    }
  );

// Type exports
export type ClinicFormData = z.infer<typeof clinicFormSchema>;
export type ClinicCreateData = z.infer<typeof clinicCreateSchema>;
export type ClinicUpdateData = z.infer<typeof clinicUpdateSchema>;
