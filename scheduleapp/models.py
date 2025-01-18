from django.db import models


class executer(models.Model):
    exe_name=models.CharField(max_length=200,null=True)
    exe_post=models.CharField(max_length=200,null=True)
    exe_code=models.CharField(max_length=200,null=True)


class task(models.Model):
    system_code=models.IntegerField(default=0,null=True)
    executer=models.CharField(max_length=200,null=True)
    executer_code=models.CharField(max_length=200,null=True)
    startdate=models.CharField(max_length=200,null=True)
    startdate_store=models.DateField(null=True)
    preiod=models.IntegerField(default=0,null=True)
    remain_date=models.IntegerField(default=0,null=True)
    enddate=models.CharField(max_length=100,null=True)
    enddate_store=models.DateField(null=True)
    finishdate=models.CharField(max_length=100,null=True)
    pariority=models.CharField(max_length=100,null=True)
    task_sub=models.CharField(max_length=100,null=True)
    task_desc=models.TextField(null=True)
    active=models.BooleanField(default=False)
    is_seen=models.BooleanField(default=False)
    progress=models.IntegerField(default=0,null=True)

class taskprogress(models.Model):
    taskcode=models.IntegerField(default=0, null=True)
    executer = models.CharField(max_length=200, null=True)
    executer_code = models.CharField(max_length=200, null=True)
    startdate = models.CharField(max_length=200, null=True)
    remain_date = models.IntegerField(default=0, null=True)
    enddate = models.CharField(max_length=100, null=True)
    finishdate = models.CharField(max_length=100, null=True)
    preiod = models.IntegerField(default=0, null=True)
    pariority = models.CharField(max_length=100, null=True)
    task_sub = models.CharField(max_length=100, null=True)
    task_desc = models.TextField(null=True)
    enterydate=models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=False)
    progress = models.IntegerField(default=0, null=True)
    attachment=models.BooleanField(default=False)
    imgsrc=models.TextField(null=True)
    notif_datetime=models.DateTimeField(auto_now_add=True,null=True)


class Image(models.Model):
    product = models.ForeignKey(taskprogress, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

class Notification(models.Model):
    notif_code = models.ForeignKey(taskprogress, on_delete=models.CASCADE,null=True)
    notif=models.CharField(max_length=100, null=True)
    exe_code=models.CharField(max_length=200, null=True)
    notif_date=models.DateTimeField(auto_now_add=True,null=True)
    is_read=models.BooleanField(default=False)

class Manager(models.Model):
    class Meta:
        permissions = (
            ('permission_code', 'Friendly permission description'),
        )
class Employee(models.Model):
    class Meta:
        permissions = (
            ('permission_code', 'Friendly permission description'),
        )








