from typing import Optional, List
from pydantic import BaseModel


# class Profile(BaseModel):
#     name: str
#     locale: str

# class Storage(BaseModel):
#     percentUsed: float

# class Metadata(BaseModel):
#     source: str
#     collectionDate: str
#     dataType: str

# class User(BaseModel):
#     userId: str
#     email: str
#     timestamp: int
#     profile: Profile
#     storage: Optional[Storage] = None
#     metadata: Optional[Metadata] = None

class PreferencesData(BaseModel):
    categories: List[str]
    likes: dict[str, bool]

class PreferencesUnrefined(BaseModel):
    address: str
    unixtime: int
    preferences: PreferencesData