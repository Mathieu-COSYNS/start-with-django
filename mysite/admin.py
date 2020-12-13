from django.contrib import admin
from .models import Comment, CommentLike, CommentReport, Confession, ConfessionLike, ConfessionReport, Hashtag, User

admin.site.register(User)
admin.site.register(Confession)
admin.site.register(Comment)
admin.site.register(Hashtag)
admin.site.register(ConfessionLike)
admin.site.register(CommentLike)
admin.site.register(ConfessionReport)
admin.site.register(CommentReport)