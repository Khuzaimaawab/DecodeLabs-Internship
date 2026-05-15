import hmac
import string

LEAKED_PASSWORDS = [b"Password123!", b"Admin@2026", b"Qwerty!99", b"Hello123"]

def check_against_leaks(password):
    raw_password = password.encode('utf-8')
    
    for leaked_entry in LEAKED_PASSWORDS:
        if len(raw_password) == len(leaked_entry):
            if hmac.compare_digest(raw_password, leaked_entry):
                return True
    return False

def get_password_strength(password):
    if len(password) < 8:
        return "WEAK: Too short (minimum 8 characters)."

    if check_against_leaks(password):
        return "WEAK: This password was found in a public leak."

    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    requirements_met = sum([has_upper, has_digit, has_special])

    if requirements_met == 3:
        return "STRONG: Great password!"
    
    if requirements_met == 2:
        return "MEDIUM: Good, but try adding a symbol or number."
    
    return "WEAK: Use a mix of uppercase, numbers, and symbols."

def run_validator():
    print("--- Password Security Check ---")
    print("(Type 'quit' to stop)\n")

    while True:
        user_input = input("Enter password: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ['quit', 'exit', 'stop']:
            print("Goodbye!")
            break

        print(f"Result: {get_password_strength(user_input)}\n")

if __name__ == "__main__":
    run_validator()