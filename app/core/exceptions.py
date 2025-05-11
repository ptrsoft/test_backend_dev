class NotFoundException(Exception):
    """Exception raised when a resource is not found."""
    def __init__(self, detail: str = "Resource not found"):
        self.detail = detail
        super().__init__(self.detail) 