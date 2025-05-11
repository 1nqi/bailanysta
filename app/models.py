from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Khabar(models.Model):
    user = models.ForeignKey(User, related_name= "khabars",on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="khabar_like", blank=True)
    

    def number_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return(f"{self.user}"
               f"({self.created_at:%Y-%m-%d %H:%M}): {self.body}...")



class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    follows = models.ManyToManyField("self", 
        related_name="followed_by",
        symmetrical=False,
        blank=True)
    github_link = models.CharField(max_length=100, blank=True, null=True)
    instagram_link = models.CharField(max_length=100, blank=True, null=True)
    telegram_link = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.user)
    

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
    else:
        pass

post_save.connect(create_profile, sender=User)

class Comment(models.Model):
    khabar = models.ForeignKey(Khabar, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('comment', 'Comment'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    khabar = models.ForeignKey(Khabar, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.notification_type == 'follow':
            return f"{self.sender.username} followed you"
        elif self.notification_type == 'like':
            return f"{self.sender.username} liked your khabar"
        elif self.notification_type == 'comment':
            return f"{self.sender.username} commented on your khabar"