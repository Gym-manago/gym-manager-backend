from app.schemas.member import MemberSchema, MemberDataPayload, MemberAddressSchema
from fastapi import APIRouter, Depends
from app.dependencies import oauth2_scheme, SessionDep

router = APIRouter(tags=["Members"], prefix="/members")


@router.post("/add", response_model=MemberSchema, dependencies=[Depends(oauth2_scheme)])
async def add_member(payload: MemberDataPayload, session: SessionDep):
    """
    Endpoint to add a new member.
    """
    member = payload.member
    address = payload.address
    address_id = MemberAddressSchema(
        **address.model_dump()) if address else None
    member = MemberSchema(**member.model_dump(),
                          address_id=address_id.id if address_id else None)
    session.add(address_id) if address_id else None
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


@router.get("/{member_id}", response_model=MemberSchema, dependencies=[Depends(oauth2_scheme)])
async def get_member(member_id: str, session: SessionDep):
    """
    Endpoint to get a member by ID.
    """
    member = session.get(MemberSchema, member_id)
    return member
