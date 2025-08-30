from django.db import models


class Skill(models.Model):

    name = models.CharField(max_length=100)
    percentage = models.IntegerField(
        default=0, help_text="Skill proficiency percentage (0-100)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-percentage', 'name']

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"



class Project(models.Model):
  
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    site_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    technologies = models.TextField(
        help_text="Comma-separated list of technologies") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        """Return technologies as a list"""
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]


class Experience(models.Model):

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.TextField(help_text="Comma-separated list of skills used")
    start_year = models.IntegerField()
    end_year = models.IntegerField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_year']
        verbose_name_plural = "Experience"

    def __str__(self):
        if self.is_current:
            return f"{self.title} at {self.company} ({self.start_year}-Present)"
        return f"{self.title} at {self.company} ({self.start_year}-{self.end_year})"

    @property
    def period_display(self):
      
        if self.is_current:
            return f"{self.start_year} - Present"
        return f"{self.start_year} - {self.end_year}"

    @property
    def skills_list(self):
        """Return skills as a list"""
        return [skill.strip() for skill in self.skills.split(',') if skill.strip()]


class Contact(models.Model):
 
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class Resume(models.Model):
 
    title = models.CharField(max_length=200, default="Resume")
    file = models.FileField(upload_to='resumes/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
