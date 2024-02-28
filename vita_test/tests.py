from django.test import TestCase

from .models import Topic, Skill, Profession


class ApiTests(TestCase):
    def test_get_all_skills_and_topics(self):
        sc1, _ = Skill.objects.get_or_create(name="test_skill1")
        sc2, _ = Skill.objects.get_or_create(name="test_skill2")
        topic1, _ = Topic.objects.get_or_create(name="test_topic1")
        sc1.topics.set([topic1])
        sc1.save()

        response = self.client.get("/api/all_skills_and_topics").json()
        self.assertTrue(any(sc['name'] == 'test_skill1' for sc in response))
        self.assertTrue(any(sc['name'] == 'test_skill2' for sc in response))
        self.assertTrue(any(topic['name'] == "test_topic1" for sc in response for topic in sc['topics']))

    def test_get_all_professions_and_skills(self):
        p1, _ = Profession.objects.get_or_create(name="test_profession1")
        p2, _ = Profession.objects.get_or_create(name="test_profession2")
        skill1, _ = Skill.objects.get_or_create(name="test_skill1")
        p1.skills.set([skill1])
        p1.save()

        response = self.client.get("/api/all_professions_and_skills").json()
        self.assertTrue(any(p1['name'] == 'test_profession1' for p1 in response))
        self.assertTrue(any(p2['name'] == 'test_profession2' for p2 in response))
        self.assertTrue(any(skill['name'] == "test_skill1" for p1 in response for skill in p1['skills']))

    def test_create_topic(self):
        response = self.client.post(
            "/api/topic",
            content_type="application/json",
            data={
                'name': "test_create_topic_test",
                "description": "string",
                "pet_project_ideas": "string",
                "useful_links": "string",
                "useful_books": "string",
                "useful_courses": "string"
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_create_duplicated_topic(self):
        data = {
            'name': "test_create_duplicated_topic",
            "description": "string",
            "pet_project_ideas": "string",
            "useful_links": "string",
            "useful_books": "string",
            "useful_courses": "string"
        }
        response = self.client.post("/api/topic", content_type="application/json", data=data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/api/topic", content_type="application/json", data=data)
        self.assertEqual(response.status_code, 422)

    def test_delete_topic(self):
        topic, _ = Topic.objects.get_or_create(name="test_delete_existing_topic")
        response = self.client.delete(f"/api/topic/{topic.id}", content_type="application/json")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.json(), {"success": True})
        self.assertFalse(Topic.objects.filter(pk=topic.id).exists())

    def test_create_skill(self):
        response = self.client.post(
            "/api/skill",
            content_type="application/json",
            data={
                "name": "test_create_skill",
                "description": "string"
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_create_duplicated_skill(self):
        data = {
            "name": "test_create_duplicated_skill",
            "description": "string"
        }
        response = self.client.post("/api/skill", content_type="application/json", data=data)
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/api/skill", content_type="application/json", data=data)
        self.assertEqual(response.status_code, 422)

    def test_create_profession(self):
        response = self.client.post(
            "/api/skill",
            content_type="application/json",
            data={
                "name": "test_create_profession",
                "description": "string"
            }
        )
        self.assertEqual(response.status_code, 200)



    def test_check_endpoint(self):
        response = self.client.get("/api/check")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
