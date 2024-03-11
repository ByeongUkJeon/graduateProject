from django.db import models

# Create your models here.

class User(models.Model):
    account = models.CharField(max_length=50, primary_key=True)
    passwd = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Tale(models.Model):
    num = models.AutoField(primary_key=True)
    imglink = models.CharField(max_length=300)
    title = models.CharField(max_length=50)
    content = models.TextField()
    likes = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(blank=True, null=True)
    reviews = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tale'


class Child(models.Model):
    num = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    type = models.CharField(max_length=20)
    personality = models.CharField(max_length=30)
    parent = models.ForeignKey('User', models.DO_NOTHING, db_column='parent')

    class Meta:
        managed = False
        db_table = 'child'



class Ttssetting(models.Model):
    num = models.AutoField(primary_key=True)
    ttsspeed = models.CharField(max_length=10)
    ttsvoice = models.CharField(max_length=10)
    childnum = models.ForeignKey(Child, models.DO_NOTHING, db_column='childnum')

    class Meta:
        managed = False
        db_table = 'ttssetting'


class Qna(models.Model):
    num = models.AutoField(primary_key=True)
    q = models.CharField(max_length=500)
    a = models.CharField(max_length=500)
    direction = models.CharField(max_length=10)
    childnum = models.ForeignKey(Child, models.DO_NOTHING, db_column='childnum')
    parent = models.ForeignKey('User', models.DO_NOTHING, db_column='parent')
    likes = models.IntegerField()
    talenum = models.ForeignKey('Tale', models.DO_NOTHING, db_column='talenum')
    writedate = models.DateTimeField(blank=True, null=True, auto_now_add = True)

    class Meta:
        managed = False
        db_table = 'qna'

class Rate(models.Model):
    num = models.AutoField(primary_key=True)
    rate = models.FloatField()
    childnum = models.ForeignKey(Child, models.DO_NOTHING, db_column='childnum')
    writedate = models.DateTimeField(blank=True, null=True, auto_now_add = True)
    talenum = models.ForeignKey('Tale', models.DO_NOTHING, db_column='talenum')

    class Meta:
        managed = False
        db_table = 'rate'


class Likes(models.Model):
    num = models.AutoField(primary_key=True)
    childnum = models.ForeignKey(Child, models.DO_NOTHING, db_column='childnum')
    talenum = models.ForeignKey('Tale', models.DO_NOTHING, db_column='talenum', related_name='likes_tale')
    writedate = models.DateTimeField(blank=True, null=True, auto_now_add = True)

    class Meta:
        managed = False
        db_table = 'likes'

class Favorite(models.Model):
    num = models.AutoField(primary_key=True)
    childnum = models.ForeignKey(Child, models.DO_NOTHING, db_column='childnum')
    talenum = models.ForeignKey('Tale', models.DO_NOTHING, db_column='talenum', related_name='favorite_tale')

    class Meta:
        managed = False
        db_table = 'favorite'

class Commentlikes(models.Model):
    num = models.AutoField(primary_key=True)
    childnum = models.ForeignKey(Child, models.DO_NOTHING, db_column='childnum')
    commentid = models.ForeignKey('Qna', models.DO_NOTHING, db_column='commentId')  # Field name made lowercase.
    writedate = models.DateTimeField(blank=True, null=True, auto_now_add = True)

    class Meta:
        managed = False
        db_table = 'commentlikes'

class RecentReads(models.Model):
    num = models.AutoField(primary_key=True)
    childnum = models.ForeignKey(Child, models.DO_NOTHING, db_column='childnum', blank=True, null=True)
    talenum = models.ForeignKey('Tale', models.DO_NOTHING, db_column='talenum', blank=True, null=True)
    readdate = models.DateTimeField(blank=True, null=True, auto_now_add = True)

    class Meta:
        managed = False
        db_table = 'recent_reads'
