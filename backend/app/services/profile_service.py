import re
from sqlalchemy.orm import Session
from app.models.profile import Profile

def update_profile_from_message(user_id: int, message: str, db: Session):

    profile = db.query(Profile).filter(Profile.user_id == user_id).first()

    if not profile:
        profile = Profile(user_id=user_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    # Detect name
    name_match = re.search(r"my name is (\w+)", message.lower())
    if name_match:
        profile.name = name_match.group(1).capitalize()

    # Detect internship
    internship_match = re.search(r"interning at ([\w\s]+)", message.lower())
    if internship_match:
        profile.internship = internship_match.group(1).title()

    # Detect university
    university_match = re.search(r"i study at ([\w\s]+)", message.lower())
    if university_match:
        profile.university = university_match.group(1).title()

    db.commit()


def build_profile_context(profile: Profile):
    if not profile:
        return ""

    context_parts = []

    if profile.name:
        context_parts.append(f"User's name is {profile.name}.")

    if profile.internship:
        context_parts.append(f"User is interning at {profile.internship}.")

    if profile.university:
        context_parts.append(f"User studies at {profile.university}.")

    return "\n".join(context_parts)
