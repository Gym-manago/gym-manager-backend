import sys
import os
# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.member import MemberSchema, MemberAddressSchema



# PostgreSQL database URL
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/gym_manager"

# Dynamically determine the path to the JSON file
current_dir = os.path.dirname(__file__)
JSON_FILE_PATH = os.path.join(current_dir, "data.json")

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()


def populate_data():
    try:
        # Read the JSON file
        with open(JSON_FILE_PATH, "r") as file:
            data = json.load(file)

        # Iterate over the array of objects
        for item in data:
            # Create a new MemberSchema object
            # Update MemberSchema and MemberAddressSchema to match the new object structure
            address = MemberAddressSchema(
                # member_id=member.id,  # Use the generated member ID
                street_line_1=item.get("address", {}).get("street_line_1"),
                street_line_2=item.get("address", {}).get("street_line_2"),
                city=item.get("address", {}).get("city"),
                state=item.get("address", {}).get("state"),
                pin_code=item.get("address", {}).get("pin_code"),
                country=item.get("address", {}).get("country"),
            )
            session.add(address)
            session.flush()  # Flush to get the member ID

            member = MemberSchema(
                first_name=item.get("member", {}).get("first_name"),
                last_name=item.get("member", {}).get("last_name"),
                email=item.get("member", {}).get("email"),
                phone_number=item.get("member", {}).get("phone_number"),
                membership_start_date=item.get(
                    "member", {}).get("membership_start_date"),
                membership_end_date=item.get(
                    "member", {}).get("membership_end_date"),
                active=item.get("member", {}).get("active"),
                date_of_birth=item.get("member", {}).get("date_of_birth"),
                gender=item.get("member", {}).get("gender"),
                membership_type=item.get("member", {}).get("membership_type"),
                address_id=address.id  # Set the foreign key to the address ID
            )
            session.add(member)


        # Commit the transaction
        session.commit()
        print("Data populated successfully.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    populate_data()
