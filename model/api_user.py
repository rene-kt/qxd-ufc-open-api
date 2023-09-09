class ApiUser:
    def __init__(self, api_key: str, name: str, email: str, is_active: bool):
        self.api_key = api_key
        self.name = name
        self.email = email
        self.is_active = is_active