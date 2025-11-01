import random
import string

def generate_verification_code(length=6):
    """Generate random verification code"""
    return ''.join(random.choices(string.digits, k=length))

def format_phone_number(phone):
    """Format phone number to standard format"""
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    # Format as (XXX) XXX-XXXX for US numbers
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone