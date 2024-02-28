from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.errors import ValidationError

from .models import Topic, Skill, Profession
from .schemas import TopicResponse, TopicSchema, SkillResponse, SkillSchema, ProfessionResponse, \
    ProfessionSchema

api = NinjaAPI()


@api.get("/check")
def check(request):
    return {"status": "ok"}


def _check_topic_name(name):
    if Topic.objects.filter(name=name).exists():
        raise ValidationError([{'name': f"This '{name}' already exist"}])


def _check_skill_name(name):
    if Skill.objects.filter(name=name).exists():
        raise ValidationError([{'name': f"This '{name}' already exist"}])


def _check_profession_name(name):
    if Profession.objects.filter(name=name).exists():
        raise ValidationError([{'name': f"This '{name}' already exist"}])


@api.post("/topic", response=TopicResponse)
def create_topic(request, payload: TopicSchema):
    _check_topic_name(payload.name)
    return Topic.objects.create(**{k: v for k, v in payload.dict().items() if v is not None})


@api.get("/topic/{topics_id}", response=TopicResponse)
def get_topic(request, topics_id: int):
    return get_object_or_404(Topic, id=topics_id)


@api.put("/topics/{topics_id}", response=TopicResponse)
def update_topic(request, topics_id: int, payload: TopicSchema):
    _check_topic_name(payload.name)
    topic = get_object_or_404(Topic, id=topics_id)
    for k, v in payload.dict().items():
        if v is not None:
            setattr(topic, k, v)
    topic.save()
    return topic


@api.delete("/topic/{topics_id}")
def delete_topic(request, topics_id: int):
    topic = get_object_or_404(Topic, id=topics_id)
    topic.delete()
    return {"success": True}


@api.post("/skill", response=SkillResponse)
def create_skill(request, payload: SkillSchema):
    _check_skill_name(payload.name)
    return Skill.objects.create(**{k: v for k, v in payload.dict().items() if v is not None})


@api.get("/skill/{skills_id}", response=SkillResponse)
def get_skill(request, skills_id: int):
    return get_object_or_404(Skill, id=skills_id)


@api.put("/skill/{skills_id}", response=SkillResponse)
def update_skill(request, skills_id: int, payload: SkillSchema):
    _check_skill_name(payload.name)
    skill = get_object_or_404(Skill, id=skills_id)
    for k, v in payload.dict().items():
        if v is not None:
            setattr(skill, k, v)
    skill.save()
    return skill


@api.put("/skill/{skills_id}/link_topic/{topic_id}", response=SkillResponse)
def link_topic_to_skills(request, skills_id: int, topic_id: int):
    skill = get_object_or_404(Skill, id=skills_id)
    skill.topics.add(get_object_or_404(Topic, id=topic_id))
    skill.save()
    return skill


@api.delete("/skill/{skills_id}")
def delete_skill(request, skills_id: int):
    skill = get_object_or_404(Skill, id=skills_id)
    skill.delete()
    return {"success": True}


@api.post("/profession", response=ProfessionResponse)
def create_profession(request, payload: ProfessionSchema):
    _check_profession_name(payload.name)
    return Profession.objects.create(**{k: v for k, v in payload.dict().items() if v is not None})


@api.get("/profession/{professions_id}", response=ProfessionResponse)
def get_profession(request, professions_id: int):
    return get_object_or_404(Profession, id=professions_id)


@api.put("/profession/{professions_id}", response=ProfessionResponse)
def update_profession(request, professions_id: int, payload: ProfessionSchema):
    _check_profession_name(payload.name)
    profession = get_object_or_404(Profession, id=professions_id)
    for k, v in payload.dict().items():
        if v is not None:
            setattr(profession, k, v)
    profession.save()
    return profession


@api.put("/skill/{skills_id}/link_profession/{professions_id}", response=ProfessionResponse)
def link_skills_to_link_profession(request, professions_id: int, skills_id: int):
    profession = get_object_or_404(Profession, id=professions_id)
    profession.skills.add(get_object_or_404(Skill, id=skills_id))
    profession.save()
    return profession


@api.delete("/profession/{professions_id}")
def delete_profession(request, professions_id: int):
    profession = get_object_or_404(Profession, id=professions_id)
    profession.delete()
    return {"success": True}


@api.get("/all_professions_and_skills")
def get_all_professions_and_skills(request):
    professions = Profession.objects.all().prefetch_related("skills", "skills__topics")
    response = []
    for profession in professions:
        profession_data = {
            "id": profession.id,
            "name": profession.name,
            "skills": [],
        }
        for skill in profession.skills.all():
            skill_data = {
                "id": skill.id,
                "name": skill.name,
                "topics": [
                    {"id": topic.id, "name": topic.name} for topic in skill.topics.all()
                ],
            }
            profession_data["skills"].append(skill_data)
        response.append(profession_data)
    return response


@api.get("/all_skills_and_topics")
def get_all_skills_and_topics(request):
    skills = Skill.objects.all().prefetch_related("topics")
    response = []
    for skill in skills:
        skill_data = {
            "id": skill.id,
            "name": skill.name,
            "topics": [{"id": topic.id, "name": topic.name} for topic in skill.topics.all()],
        }
        response.append(skill_data)
    return response
