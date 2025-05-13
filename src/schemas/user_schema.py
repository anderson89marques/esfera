from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
    email: str
    model_config = ConfigDict(from_attributes=True)

class AddressSchema(BaseModel):
    street: str
    city: str
    state: str
    zipcode: str
    country: str
    user: UserSchema
    model_config = ConfigDict(from_attributes=True)

class UserEventSchema(BaseModel):
    user_id: int
    event_timestamp: datetime

class UserList(BaseModel):
    users: list[UserSchema]

class AddressList(BaseModel):
    addresses: list[AddressSchema]

class EventList(BaseModel):
    events: list[UserEventSchema]
