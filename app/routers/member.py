from app.schemas.member import MemberSchema, MemberDataPayload, MemberAddressSchema
from sqlmodel import select
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import oauth2_scheme, SessionDep

router = APIRouter(tags=["Members"], prefix="/members")


@router.post("/add", response_model=MemberSchema, dependencies=[Depends(oauth2_scheme)])
async def add_member(payload: MemberDataPayload, session: SessionDep):
    """
    Endpoint to add a new member.
    """
    member = payload.member
    address = payload.address
    try:
        address_id = MemberAddressSchema(
            **address.model_dump()) if address else None
        member = MemberSchema(**member.model_dump(),
                              address_id=address_id.id if address_id else None)
        session.add(address_id) if address_id else None
        session.add(member)
        session.commit()
        session.refresh(member)
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"{'Unique constraint violation' if 'unique constraint' in str(e.__cause__) else 'Invalid credentials'}"
        )
    return member


@router.get("/get-all", response_model=list[MemberSchema], dependencies=[Depends(oauth2_scheme)])
async def get_all_members(session: SessionDep):
    getAllStatement = select(MemberSchema)
    members = session.exec(getAllStatement).all()
    return members


@router.get("/{member_id}", response_model=MemberDataPayload, dependencies=[Depends(oauth2_scheme)])
async def get_member(member_id: str, session: SessionDep):
    """
    Endpoint to get a member by ID.
    """
    member = session.get(MemberSchema, member_id)
    address = session.get(
        MemberAddressSchema, member.address_id) if member and member.address_id else None
    return {"member": member, "address": address}

# TODO: Implement update and delete endpoints for members.
