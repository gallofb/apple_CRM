from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    # """客户信息表"""
    name = models.CharField(max_length=32,blank=True,null=True)
    qq = models.CharField(max_length=32,unique=True)   #unique=True指的这个字段在这张表中不能重复
    qq_name = models.CharField(max_length=64,blank=True,null=True)
    phone = models.CharField(max_length=32,blank=True,null=True)
    source_choice = ((0,'转介绍'),
                     (1,'qq群'),
                     (2,'官网'),
                     (3,'百度'),
                     (4,'市场推销'),
                     (5,'知乎'))
    source = models.SmallIntegerField(choices=source_choice) #选项
    #转介绍人 verbose_name 指明一个易于理解和表述的对象名称
    referral_from = models.CharField(verbose_name="转介绍人qq",max_length=64,blank=True,null=True)
    consult_course = models.ForeignKey("Course",verbose_name="咨询课程",on_delete=models.CASCADE)
    #标签
    content = models.TextField(verbose_name="咨询详情")
    tags = models.ManyToManyField("Tag",blank=True)
    # 备注
    status_choice = ((0,"已报名"),
                     (1,'未报名'),)

    status = models.SmallIntegerField(choices=source_choice,default=1)
    note = models.CharField(max_length=64,blank=True,null=True)
    #销售顾问
    consultant = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)  #时间自增

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name_plural = "客户信息表"

class Tag(models.Model):
    """标签"""
    name = models.CharField(unique=True,max_length=32)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "标签"

class CustomerFollowUp(models.Model):
    """客户跟进表"""
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)   #客户
    content = models.TextField(verbose_name="跟进内容")
    consultant = models.ForeignKey("UserProfile",on_delete=models.CASCADE)   #跟进人员
    date = models.DateTimeField(auto_now_add=True)
    #客户情况
    intention_choice = ((0,"2周内报名"),
                        (1,"一月内报名"),
                        (2,"近期无报名计划"),
                        (3,"已在其他机构报名"),
                        (4,"已报名"),
                        (5,"已拉黑"),
                        )
    intention = models.SmallIntegerField(choices=intention_choice)

    def __str__(self):
        return "<%s : %s>" %(self.customer.qq,self.intention)

    class Meta:
        verbose_name_plural = "客户跟进表"

class UserProfile(models.Model):
    """角色表"""
    user = models.OneToOneField(User,on_delete=models.CASCADE)   #关联django 自带的表
    name = models.CharField(max_length=32)
    roles = models.ManyToManyField("Role",blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "角色表"
#学习与上课是一对多
class CourseRecord(models.Model):
    """上课记录表"""
    from_class = models.ForeignKey("ClassList",on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name="第几节(天)")
    teacher = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    has_homework = models.BooleanField(default=True)
    homework_title = models.CharField(max_length=128,blank=True,null=True)
    homework_content = models.TextField(blank=True,null=True)
    outline = models.TextField(verbose_name="本节课程大纲")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.from_class,self.day_num)

    #联合唯一   同时出现
    class Meta:
        unique_together = ("from_class","day_num")
        verbose_name_plural = "上课记录表"

class StudyRecord(models.Model):
    """学习记录"""
    student = models.ForeignKey("Enrollment",on_delete=models.CASCADE)
    course_record =models.ForeignKey("CourseRecord",on_delete=models.CASCADE)
    attendance_choicee = ((0,"已签到"),
                          (1,"迟到"),
                          (2,"缺勤"),
                          (3,"早退"),)
    attendance = models.SmallIntegerField(choices=attendance_choicee,default=0)
    #成绩
    score_choices = ((100,"A+"),
                     (90,"A"),
                     (85,"B+"),
                     (80,"B"),
                     (75,"B-"),
                     (70,"C+"),
                     (60,"C"),
                     (40,"C-"),
                     (-50,"D"),
                     (-100,"COPY"),
                     (0,"N/A"),)   #没上
    score = models.SmallIntegerField(choices=score_choices)
    memo = models.TextField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s %s" %(self.student,self.course_record,self.score)

    class Meta:
        unique_together = ('student','course_record')
        verbose_name_plural = "学习记录"

class Branch(models.Model):
    """分区"""
    name = models.CharField(max_length=64,unique=True)
    addr = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = "分区"

class ClassList(models.Model):
    """班级表"""
    branch = models.ForeignKey("Branch",verbose_name="校区",on_delete=models.CASCADE)
    course = models.ForeignKey("Course",on_delete=models.CASCADE)
    class_type_choice = (
                         (0,'面授(周中)'),
                         (1,'面授(周末)'),
                         (2,'网络'),
                         )
    class_type = models.SmallIntegerField(choices=class_type_choice,verbose_name="课程类型")
    semester = models.PositiveIntegerField(verbose_name="学期")
    teachers = models.ManyToManyField("UserProfile")  #一节课可能有多个老师上
    start_date = models.DateField(verbose_name="开班日期")
    end_date = models.DateField(verbose_name="结课日期",blank=True,null=True)

    def __str__(self):
        #校区 课程 第几期
        return "%s %s %s" %(self.branch,self.course,self.semester)
    #联合唯一
    class Meta:
        unique_together = ('branch','course','semester')
        verbose_name_plural = "班级表"

class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=64,unique=True)
    price = models.PositiveIntegerField() #正数
    period = models.PositiveIntegerField(verbose_name="周期(月)")
    outline = models.TextField()  #课程大纲

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "课程表"

class Enrollment(models.Model):
    """报名表"""
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    enrolled_class = models.ForeignKey("ClassList",verbose_name="所报班级",on_delete=models.CASCADE)
    consultant = models.ForeignKey("UserProfile",verbose_name="课程顾问",on_delete=models.CASCADE)
    contract_agreed = models.BooleanField(default=False,verbose_name="学员同意合同")
    contract_approved = models.BooleanField(default=False,verbose_name="合同以审核")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.customer,self.enrolled_class)

    class Meta:
        unique_together = ("customer","enrolled_class")
        verbose_name_plural = "报名表"

class Pyment(models.Model):
    """缴费记录"""
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    course = models.ForeignKey("Course",verbose_name="所报课程",on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name="数额",default=500)
    consultant = models.ForeignKey("UserProfile",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.customer,self.amount)
    class Meta:
        verbose_name_plural = "缴费记录"
        verbose_name = "缴费记录"



class Role(models.Model):
    """权限表"""
    name = models.CharField(max_length=32,unique=True)
    menus = models.ManyToManyField("Menu",blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "权限表"

class Menu(models.Model):
    """菜单"""
    name = models.CharField(max_length=32)
    #存放url的别名
    url_name = models.CharField(max_length=64,unique=True)

    def __str__(self):
        return self.name