from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ApiResponse:
    success: bool = True
    message: str = ""
    data: Any = None
    errors: list = field(default_factory=list)

    def to_dict(self):
        result = {"success": self.success}
        if self.message:
            result["message"] = self.message
        if self.data is not None:
            result["data"] = self.data
        if self.errors:
            result["errors"] = self.errors
        return result

    @classmethod
    def ok(cls, data=None, message=""):
        return cls(success=True, data=data, message=message)

    @classmethod
    def error(cls, message, errors=None):
        return cls(success=False, message=message, errors=errors or [])


@dataclass
class PaginatedResponse:
    items: list = field(default_factory=list)
    total: int = 0
    page: int = 1
    per_page: int = 12
    total_pages: int = 0

    def __post_init__(self):
        if self.total > 0 and self.per_page > 0:
            self.total_pages = (self.total + self.per_page - 1) // self.per_page
