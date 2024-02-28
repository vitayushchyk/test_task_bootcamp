from typing import Optional

from ninja import Schema


class TopicSchema(Schema):
    name: str
    description: Optional[str] = None
    pet_project_ideas: Optional[str] = None
    useful_links: Optional[str] = None
    useful_books: Optional[str] = None
    useful_courses: Optional[str] = None


class TopicResponse(Schema):
    pk: int


class SkillSchema(Schema):
    name: str
    description: Optional[str] = None


class SkillResponse(Schema):
    pk: int


class ProfessionSchema(Schema):
    name: str
    description: Optional[str] = None


class ProfessionResponse(Schema):
    pk: int
