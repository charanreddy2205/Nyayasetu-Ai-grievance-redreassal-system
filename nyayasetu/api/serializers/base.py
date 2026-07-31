from django.core.exceptions import ValidationError
from typing import Any, Dict, List, Optional, Union

class BaseSerializer:
    """
    Lightweight, high-performance BaseSerializer mimicking standard serializer layers.
    Provides automated model representation mapping and custom payload validation hooks.
    """
    def __init__(
        self,
        instance: Any = None,
        data: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        self.instance = instance
        self.data = data
        self.context = context or {}
        self._errors: Dict[str, List[str]] = {}

    def is_valid(self) -> bool:
        """
        Executes custom validate hook and returns True if no validation errors occur.
        """
        self._errors = {}
        if self.data is None:
            self._errors["non_field_errors"] = ["No input parameters provided."]
            return False
        try:
            self.validate()
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                self._errors.update(e.message_dict)
            else:
                self._errors["non_field_errors"] = e.messages
        return len(self._errors) == 0

    @property
    def errors(self) -> Dict[str, List[str]]:
        """
        Returns validation error dictionary mapping.
        """
        return self._errors

    def validate(self) -> None:
        """
        Hooks custom validation logic. Raise django.core.exceptions.ValidationError on failure.
        """
        pass

    def to_representation(self, instance: Any) -> Dict[str, Any]:
        """
        Maps model instance attributes to a plain JSON-compatible dictionary.
        """
        raise NotImplementedError

    @property
    def serialized_data(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Dynamically serializes single model records or lists/querysets.
        """
        if self.instance is None:
            return {}
            
        # Check if instance is a list/queryset or single object
        if hasattr(self.instance, '__iter__') and not isinstance(self.instance, dict):
            return [self.to_representation(obj) for obj in self.instance]
        return self.to_representation(self.instance)
