from sqlmodel import SQLModel, Field, Enum as SQLEnum, Column
from enum import Enum
from uuid import UUID, uuid4


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    NOT_SPECIFIED = "Not Specified"


class MembershipType(str, Enum):
    GYM = "Gym"
    SWIMMING = "Swimming"


class MemberAddressPayload(SQLModel):
    street_line_1: str
    street_line_2: str | None = None
    city: str
    state: str
    pin_code: str
    country: str


class MemberAddressSchema(MemberAddressPayload, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    # member_id: UUID | None = Field(default=None, foreign_key="memberschema.id")


class MemberPayload(SQLModel):
    first_name: str
    last_name: str
    email: str = Field(index=True)
    phone_number: str | None = None
    membership_start_date: str
    membership_end_date: str
    active: bool = True
    date_of_birth: str | None = None
    gender: Gender = Field(default=Gender.NOT_SPECIFIED,
                           sa_column=Column(SQLEnum(Gender)))
    membership_type: MembershipType = Field(default=MembershipType.GYM,
                                            sa_column=Column(SQLEnum(MembershipType)))


class MemberDataPayload(SQLModel):
    member: MemberPayload
    address: MemberAddressPayload | None = None


class MemberSchema(MemberPayload, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    address_id: UUID | None = Field(
        default=None, foreign_key="memberaddressschema.id")
