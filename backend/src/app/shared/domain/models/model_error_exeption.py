class ModelErrorException(Exception):
    """
    Custom exception for model errors, including property name and error message.
    """

    def __init__(self, property_name: str, user_message: str = "Invalid data", developer_message: str = ""):
        self.property_name = property_name
        self.user_message = user_message
        self.developer_message = developer_message
        super().__init__(f"Invalid '{property_name}'")

    def primitives(self) -> dict:
        return {
            "property": self.property_name,
            "user_message": self.user_message,
            "developer_message": self.developer_message
        }
