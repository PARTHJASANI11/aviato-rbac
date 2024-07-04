from enum import Enum
import sqlalchemy

class SortEnum(str, Enum):
    """
    Enum class to define sort type 
    """
    ASC = "asc"
    DESC = "desc"

# Sort type mapping with sqlalchemy
SORT_TYPE = {"asc": sqlalchemy.asc, "desc": sqlalchemy.desc}