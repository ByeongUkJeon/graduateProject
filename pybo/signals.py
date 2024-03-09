# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from pybo.models import Likes, Tale, Qna
#
# @receiver(post_save, sender=Likes)
# def update_post_likes_count(sender, instance, created, **kwargs):
#     if created:
#         tale = instance.talenum
#         tale.likes += 1
#         tale.save()
#
# @receiver(post_delete, sender=Likes)
# def update_tale_likes_count_on_delete(sender, instance, **kwargs):
#     tale = instance.talenum
#     tale.likes -= 1
#     tale.save()
#
# @receiver(post_save, sender=Qna)
# def update_post_likes_count(sender, instance, created, **kwargs):
#     if created:
#         tale = instance.talenum
#         tale.reviews += 1
#         tale.save()
#
# @receiver(post_delete, sender=Qna)
# def update_tale_likes_count_on_delete(sender, instance, **kwargs):
#     tale = instance.talenum
#     tale.reviews -= 1
#     tale.save()