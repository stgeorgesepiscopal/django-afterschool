from django.db import models

class DayofWeek(models.Model):
	MONDAY = '0'
	TUESDAY = '1'
	WEDNESDAY = '2'
	THURSDAY = '3'
	FRIDAY = '4'
	DOW_CHOICES = (
		(MONDAY, 'Monday'),
		(TUESDAY, 'Tuesday'),
		(WEDNESDAY, 'Wednesday'),
		(THURSDAY, 'Thursday'),
		(FRIDAY, 'Friday'),

	)
	day = models.CharField(max_length=2, choices=DOW_CHOICES)

	class Meta:
		verbose_name = 'day_of_week'
		verbose_name_plural = 'days_of_the_week'
		#app_label = 'afterschool.students'

	def __str__(self):
		if self.day == '0':
			return 'Monday'
		elif self.day == '1':
			return 'Tuesday'
		elif self.day == '2':
			return 'Wednesday'
		elif self.day == '3':
			return 'Thursday'
		elif self.day == '4':
			return 'Friday'
		else:
			return 'ERROR'


class Student(models.Model):
	name = models.CharField(max_length=60)
	grade = models.SmallIntegerField()
	schedule = models.ManyToManyField(DayofWeek, related_name='students')
	
	class Meta:
		verbose_name = 'student'
		verbose_name_plural = 'students'
		#app_label = 'afterschool.students'

	def __str__(self):
		return self.name + ' ('+str(self.grade)+')'


class Family(models.Model):
	name = models.CharField(max_length=60)
	children = models.ManyToManyField(Student, related_name='families', related_query_name='family')

	class Meta:
		verbose_name = 'family'
		verbose_name_plural = 'families'
		#app_label = 'afterschool.students'

	def __str__(self):
		return self.name + ' (' + ','.join([str(child) for child in self.children.all()]) + ')'

class Session(models.Model):
	start = models.DateTimeField()
	end = models.DateTimeField(null=True)
	student = models.ForeignKey(Student, related_name='sessions', on_delete=models.SET_NULL, null=True)
	parent = models.CharField(max_length=60,null=True)

	class Meta:
		verbose_name = 'session'
		verbose_name_plural = 'sessions'
		#app_label = 'afterschool.students'

	@property
	def duration(self):
		"Returns the duration of the session in minutes"
		if self.end is None:
			return 0
		else:
			return (self.end - self.start).total_seconds() / 60

	def __str__(self):
		return str(self.student) + ' ' + self.start.strftime('%x')
