import secrets

import mptt
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def user_can_vote(self, user):
        """
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = [
                'primary',
                'secondary',
                'success',
                'danger',
                'dark',
                'warning',
                'info',
            ]

            d['alert_class'] = secrets.choice(alert_class)
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (
                    choice.get_vote_count / self.get_vote_count
                ) * 100

            res.append(d)
        return res

    def __str__(self):
        return self.text


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.text[:25]} - {self.choice_text[:25]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.poll.text[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'


class Genre(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    class MPTTMeta:
        order_insertion_by = ['name']


class SampleData(models.Model):
    pk_id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(null=True, blank=True)
    market_id = models.IntegerField(null=True, blank=True)
    ppg = models.CharField(max_length=255, null=True, blank=True)
    retailer = models.CharField(max_length=255, null=True, blank=True)
    nsv_cal = models.FloatField(null=True, blank=True)
    list_price_cal = models.FloatField(null=True, blank=True)
    list_price_cal_new = models.FloatField(null=True, blank=True)
    list_price_cal_per_change_ip = models.FloatField(null=True, blank=True)
    base_price_cal = models.FloatField(null=True, blank=True)
    base_price_cal_new = models.FloatField(null=True, blank=True)
    base_price_cal_per_change_ip = models.FloatField(null=True, blank=True)
    aup_cal = models.FloatField(null=True, blank=True)
    aup_cal_new = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.ppg + " - " + self.retailer


class SampleDataMptt(MPTTModel):
    datarow = models.ForeignKey(
        SampleData, null=True, blank=True, on_delete=models.CASCADE
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    class MPTTMeta:
        order_insertion_by = ['datarow']
