from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Skill, Project, Experience, Contact, Resume
from .serializers import (
    SkillSerializer, ProjectSerializer,
    ExperienceSerializer, ContactSerializer, ResumeSerializer
)
from django.http import FileResponse
import os
from django.conf import settings
from django.core.mail import send_mail


@api_view(['GET', 'POST'])
def get_skills(request):
   if request.method == 'GET':
    skills = Skill.objects.all()
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)
   elif request.method == 'POST':
    serializer = SkillSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

@api_view(['PUT'])
def update_skill(request, pk):
    try:
        skill = Skill.objects.get(pk=pk)
    except Skill.DoesNotExist:
        return Response({'error': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = SkillSerializer(skill, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

@api_view(['GET', 'POST'])
def get_projects(request):
   if request.method == 'GET':
    project = Project.objects.all()
    serializer = ProjectSerializer(project, many=True)
    return Response(serializer.data)
   elif request.method == 'POST':
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({'error': 'project not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer(project, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_experience(request):
   if request.method == 'GET':
    current = request.query_params.get('current', None)
    if current is not None:
        experience = Experience.objects.filter(
            is_current=current.lower() == 'true')
    else:
        experience = Experience.objects.all()
        # experience = Experience.objects.all()
        serializer = ExperienceSerializer(experience, many=True)
    return Response(serializer.data)
   elif request.method == 'POST':
    serializer = ExperienceSerializer(data=request.data) 
    if serializer.is_valid():
        serializer.save() 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_experience(request, pk):
    try:
        experience = Experience.objects.get(pk=pk)
    except Experience.DoesNotExist:
        return Response({'error': 'experience not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ExperienceSerializer(experience, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def contact_submission(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Send Email to your Gmail
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            phone = serializer.validated_data['phone']
            message = serializer.validated_data['message']

            send_mail(
                subject=f"New Message: From {first_name}",
                message=f"From: {first_name} {last_name} <{email}>\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL], 
                fail_silently=False,
            )
            return Response({"message": "Submitted successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        messages = Contact.objects.all().order_by('-created_at')
        serializer = ContactSerializer(messages, many=True)
        return Response(serializer.data)



@api_view(['POST'])
def resume_upload(request):
    serializer = ResumeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def download_resume(request):
  
    resume = get_object_or_404(Resume, is_active=True)

    file_path = os.path.join(settings.MEDIA_ROOT, str(resume.file))
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{resume.title}.pdf"'
        return response
    return Response({'error': 'Resume file not found'}, status=status.HTTP_404_BAD_REQUEST)
