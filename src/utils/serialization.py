from dataclasses import asdict, fields, is_dataclass
from src.models.inventory import Location
from enum import Enum

def serialize(obj):
    """
    Recursively converts a Python object into a JSON-compatible format.

    Handles:
    - Enums: Serialized as their `name`.
    - Dataclasses: Serialized into dictionaries by recursively serializing their fields.
    - Lists and Sets: Serialized into lists, with each element serialized recursively.
    - Dictionaries: Keys and values are serialized recursively. If the keys are `Location` objects,
      they are converted to strings using `location_to_string`.
    - Class objects: Serialized as their `__name__`.
    - Primitives: Returned as-is.

    Parameters:
        obj: The object to serialize.

    Returns:
        A JSON-compatible representation of the object.
    """
    if isinstance(obj, Enum):  # Handle Enums
        return obj.name
    elif is_dataclass(obj):  # Handle dataclasses
        return {field.name: serialize(getattr(obj, field.name)) for field in fields(obj)}
    elif isinstance(obj, list):  # Handle lists
        return [serialize(item) for item in obj]
    elif isinstance(obj, set):  # Handle sets
        return [serialize(item) for item in obj]
    elif isinstance(obj, dict):  # Handle dictionaries
        if all(isinstance(k, Location) for k in obj.keys()):  # Convert Location keys
            return {location_to_string(k): serialize(v) for k, v in obj.items()}
        return {serialize(key): serialize(value) for key, value in obj.items()}
    elif isinstance(obj, type):  # Handle class objects
        return obj.__name__
    else:  # Handle primitives
        return obj


def deserialize(data, cls):
    """
    Recursively converts a dictionary to a dataclass instance.

    Parameters:
        data: The dictionary to deserialize.
        cls: The dataclass type to convert into.

    Returns:
        An instance of the specified dataclass.
    """
    if isinstance(data, dict) and is_dataclass(cls):
        kwargs = {}
        for field in fields(cls):
            field_type = field.type
            field_value = data.get(field.name)

            # Handle nested dataclasses
            if is_dataclass(field_type):
                kwargs[field.name] = deserialize(field_value, field_type)
            # Handle lists of nested dataclasses
            elif hasattr(field_type, "__origin__") and field_type.__origin__ is list:
                subtype = field_type.__args__[0]
                kwargs[field.name] = [deserialize(item, subtype) for item in field_value]
            # Handle dictionaries with Location keys
            elif hasattr(field_type, "__origin__") and field_type.__origin__ is dict:
                key_type, value_type = field_type.__args__
                if key_type == Location:
                    kwargs[field.name] = {
                        string_to_location(k): deserialize(v, value_type)
                        for k, v in field_value.items()
                    }
                else:
                    kwargs[field.name] = {
                        deserialize(k, key_type): deserialize(v, value_type)
                        for k, v in field_value.items()
                    }
            # Handle sets
            elif hasattr(field_type, "__origin__") and field_type.__origin__ is set:
                subtype = field_type.__args__[0]
                kwargs[field.name] = {deserialize(item, subtype) for item in field_value}
            # Handle Enums
            elif issubclass(field_type, Enum):
                kwargs[field.name] = field_type[field_value]
            else:
                kwargs[field.name] = field_value

        return cls(**kwargs)
    else:
        return data
    

# Helper functions for Location fidelity

def location_to_string(location):
    """
    Converts a Location object to a string for use as a JSON key.
    """
    return f"{location.boxname}({location.row},{location.col}):{location.label}:{location.sidelabel}"


def string_to_location(location_str):
    """
    Converts a string representation of a Location back into a Location object.

    Parameters:
        location_str: The string representation of a Location.

    Returns:
        A Location object.

    Raises:
        ValueError: If the string cannot be parsed into a Location.
    """
    # Ensure the string contains the expected number of parts
    parts = location_str.split(":")
    if len(parts) != 4:
        raise ValueError(f"Invalid Location string format: {location_str}")

    # Parse the boxname and coordinates
    box_info, row_col, label, sidelabel = parts
    if "(" not in box_info or ")" not in box_info:
        raise ValueError(f"Invalid boxname or coordinates in Location string: {location_str}")

    boxname = box_info.split("(")[0]
    coordinates = box_info.split("(")[1].strip(")").split(",")

    if len(coordinates) != 2:
        raise ValueError(f"Invalid row,col format in Location string: {location_str}")

    # Parse row and column as integers
    try:
        row = int(coordinates[0])
        col = int(coordinates[1])
    except ValueError:
        raise ValueError(f"Row and column must be integers in Location string: {location_str}")

    # Construct and return the Location object
    return Location(boxname=boxname, row=row, col=col, label=label, sidelabel=sidelabel)
