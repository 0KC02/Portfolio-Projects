import random
import string
import re

class PasswordGenerator:
    @staticmethod
    def generate(length=16, include_uppercase=True, include_lowercase=True, 
                 include_numbers=True, include_symbols=True):
        """Generate a random password with specified criteria"""
        characters = ""
        
        if include_lowercase:
            characters += string.ascii_lowercase
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_numbers:
            characters += string.digits
        if include_symbols:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not characters:
            raise ValueError("At least one character type must be selected")
        
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

class PasswordStrength:
    @staticmethod
    def analyze(password):
        """Analyze password strength and return score and feedback"""
        score = 0
        feedback = []
        
        if len(password) == 0:
            return 0, "Very Weak", "#FF0000", ["Password is empty"]
        
        # Length checks
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")
        
        if len(password) >= 12:
            score += 1
        else:
            feedback.append("Consider using 12+ characters for better security")
        
        # Character variety checks
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if re.search(r'[0-9]', password):
            score += 1
        else:
            feedback.append("Add numbers")
        
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 1
        else:
            feedback.append("Add special characters")
        
        # Complexity checks
        if len(password) >= 16:
            score += 1
        
        if len(set(password)) >= len(password) * 0.7:  # Good character variety
            score += 1
        
        # Determine strength level
        if score <= 2:
            strength = "Very Weak"
            color = "#FF0000"
        elif score <= 4:
            strength = "Weak"
            color = "#FF6600"
        elif score <= 6:
            strength = "Fair"
            color = "#FFCC00"
        elif score <= 7:
            strength = "Good"
            color = "#66CC00"
        else:
            strength = "Strong"
            color = "#00CC00"
        
        return score, strength, color, feedback if feedback else ["Password meets all criteria!"]

