from django.db import models
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher as bc
from django.utils.timezone import now


class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    img_path = models.CharField(default='images/anonymous.jpg', max_length=64)
    location = models.CharField(default='', max_length=64)
    title = models.CharField(default='', max_length=64)
    about = models.TextField(default='')
    reputation = models.IntegerField(default=0)

    created_at = models.DateTimeField(default=now())
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def check_user(username, password):
        try:
            user = User.objects.get(username=username)
        except:
            return False
        return bc().verify(password, user.password)

    def set_hash_password(self, password: str):
        hasher = bc()
        self.password = hasher.encode(password, hasher.salt())


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)
    text = models.CharField(default='', max_length=256)
    count = models.IntegerField(default=1)


class Question(models.Model):
    title = models.CharField(max_length=128)
    votes = models.IntegerField(default=0) 
    views = models.IntegerField(default=0)
    text = models.TextField()

    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=now())
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    text = models.TextField()
    likes = models.IntegerField(default=0)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=now())
    updated_at = models.DateTimeField(auto_now=True)

