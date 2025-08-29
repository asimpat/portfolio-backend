from rest_framework import serializers
from .models import Skill, Project, Experience, Contact, Resume


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'percentage', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    tech_list = serializers.ReadOnlyField()

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'image', 'site_url', 'github_url',
                  'technologies', 'tech_list', 'created_at', 'updated_at']


class ExperienceSerializer(serializers.ModelSerializer):
    period_display = serializers.ReadOnlyField()
    skills_list = serializers.ReadOnlyField()

    class Meta:
        model = Experience
        fields = ['id', 'title', 'company', 'description', 'skills', 'skills_list',
                  'start_year', 'end_year', 'is_current', 'period_display',
                  'created_at', 'updated_at']


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'email', 'phone',
                  'message', 'created_at']


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'title', 'file',
                  'is_active', 'created_at', 'updated_at']
