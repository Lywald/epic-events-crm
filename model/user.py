class User:
    def __init__(self, id: int, email: str, password_hash: str,
                 employee_number: int, name: str, 
                 affiliation: str, permissions: str):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.employee_number = employee_number
        self.name = name
        self.affiliation = affiliation
        self.permissions = permissions

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "password_hash": self.password_hash,
            "employee_number": self.employee_number,
            "name": self.name,
            "affiliation": self.affiliation,
            "permissions": self.permissions
        }