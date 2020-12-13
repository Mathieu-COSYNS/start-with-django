from django.db import models


class User(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email


class Confession(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(max_length=1000)
    hashtags = models.ManyToManyField("Hashtag", blank=True)

    def __str__(self):
        if len(self.title) > 40:
            return self.title[:40] + "..."
        return self.title


class Comment(models.Model):
    content = models.TextField(max_length=300)
    confession = models.ForeignKey("Confession", on_delete=models.CASCADE)
    author = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        if len(self.content) > 40:
            return self.content[:40] + "..."
        return self.content


class Hashtag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ConfessionLike(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    confession = models.ForeignKey("Confession", on_delete=models.CASCADE)
    positive = models.BooleanField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "confession"], name="user_confession_constraint")]

    def __str__(self):
        return str(self.user) + " " + str(self.confession) + " " + str(self.positive)


class CommentLike(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    positive = models.BooleanField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "comment"], name="user_comment_constraint")]

    def __str__(self):
        return str(self.user) + " " + str(self.comment) + " " + str(self.positive)


class ConfessionReport(models.Model):
    confession = models.OneToOneField("Confession", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return str(self.confession) + " " + str(self.count)


class CommentReport(models.Model):
    comment = models.OneToOneField("Comment", on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return str(self.comment) + " " + str(self.count)
