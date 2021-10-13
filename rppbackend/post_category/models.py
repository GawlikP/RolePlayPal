from django.db import models

class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    populatity = models.IntegerField(default=0)
    class Meta:
       ordering = ('name',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    
