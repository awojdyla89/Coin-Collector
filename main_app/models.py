from django.db import models
# Import the reverse function
from django.urls import reverse
from datetime import date
# import the user
from django.contrib.auth.models import User

APPOINTMENTS = (
    ('M', 'Morning' ),
    ('A', 'Afternoon'),
    ('E', 'Evening'),
)

class Grading(models.Model):
    grading = models.CharField(max_length=50)
    luster = models.CharField(max_length=20)

    def __str__(self):
        return self.grading

    def get_absolute_url(self):
        return reverse('gradings_detail', kwargs={'pk': self.id})

# Create your models here.
class Coin(models.Model):
    name = models.CharField(max_length=100)
    metallurgy = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    # Add the M:M relationship
    gradings = models.ManyToManyField(Grading)
    # Add the foreign key linking to a user instance
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
  # Add this method
    def get_absolute_url(self):
        return reverse('detail', kwargs={'coin_id': self.id})
    
    def appraised_for_today(self):
        return self.appraisals_set.filter(date=date.today()).count() >= len(APPOINTMENTS)


class Appraisals(models.Model):
    date = models.DateField('Appraisal Date')
    appointment = models.CharField('Time Of Day',
        max_length=1,
        # add the 'choices' field option
        choices=APPOINTMENTS,
        # set the default value for meal to be 'M'
        default=APPOINTMENTS[0][0]
        )

    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)    

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_appointment_display()} on {self.date}"
    
    # change the default sort
    class Meta:
        ordering = ['-date']