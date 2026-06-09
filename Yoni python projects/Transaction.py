import json
import os


# ==========================================
# 1. CLASS DEFINITION
# ==========================================
class Transaction:
    def __init__(self, t_type, amount, date, description, category=None):
        self.type = t_type.lower()
        self.amount = float(amount)
        self.date = date
        self.description = str(description)
        self.category = category

    def display(self):
        base_info = f"{self.type.title()}: ${self.amount:.2f} | Date: {self.date} | Desc: {self.description}"
        if self.category:
            return base_info + f" | Category: {self.category}"
        return base_info

    def to_dict(self):
        return {
            "type": self.type,
            "amount": self.amount,
            "date": self.date,
            "description": self.description,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["type"], data["amount"], data["date"], data["description"], data.get("category"))



