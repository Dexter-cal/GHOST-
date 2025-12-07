import random
import string

class PasswordGenerator:
    """
    Generates strong passwords using a variety of strategies to mimic
    different user behaviors.
    """
    def __init__(self):
        # In a real system, these would be loaded from larger files.
        self.wordlist = ["correct", "horse", "battery", "staple", "ghost", "stealth", "digital", "phantom"]

    def generate_password(self, strategy="random", length=16):
        """
        Generates a password based on the specified strategy.
        """
        if strategy == "memorable":
            return self._generate_memorable_password()
        elif strategy == "pattern":
            return self._generate_pattern_password()
        else: # Default to random
            return self._generate_random_password(length)

    def _generate_random_password(self, length):
        """High-entropy random password."""
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))

    def _generate_memorable_password(self):
        """Generates a password from a wordlist, xkcd-style."""
        words = random.sample(self.wordlist, k=min(4, len(self.wordlist)))
        return "-".join(word.capitalize() for word in words)

    def _generate_pattern_password(self):
        """Generates a password that mimics a common user pattern."""
        word = random.choice(self.wordlist).capitalize()
        year = random.randint(2020, 2025)
        special_char = random.choice("!@#$%^&*")
        return f"{word}{year}{special_char}"
