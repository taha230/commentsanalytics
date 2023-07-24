# -*- encoding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from enum import Enum
import uuid

# Create your models here.
class Payment_Type(Enum):
    VISA_CARD = "Visa Card"
    PAYPALL = "Paypal"
    MASTER_CARD = "Master Card"
    STRIPE = "Stripe"
    WEBMONEY = "Web Money"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Request_Type(Enum):

    SENTIMENT_ANALYSIS = "Sentiment Analysis"
    KEYWORD_EXTRACTION = "Keyword Extraction"
    NAMED_ENTITY_RECOGNITION = "Named-Entity Recognition"
    YOUTUBE_CATEGORY_EXTRACTION = "Youtube-Category Extraction"



    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Request_Process_Status(Enum):

    NONE = "None"
    FALSE = "False"
    PROCESS = "Process"
    TRUE = "True"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Request_Run_Type(Enum):
    BULK = "Bulk"
    SINGLE = "Single"
    DEMO = "Demo"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Request_Status(Enum):
    SUCCESS = "Success"
    FAILED = "Failed"
    IN_QUEUE = "In Queue"
    PENDING = "Pending"


    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Bulk_Status(Enum):
    IN_QUEUE = "In Queue"
    FAILED = "Failed"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Payment_Status(Enum):
    CANCEL = "Cancel"
    SUCCESS = "Success"
    PAYMENT_FAILED = "Payment Failed"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Plan_Status(Enum):
    ENABLE = "Enable"
    DISABLE = "Disable"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Post_Status(Enum):
    PUBLISHED = "Published"
    UNPUBLISHED = "Unpublished"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Ticket_Status(Enum):
    USER_ANSWERED = "User Answered" # in the case of user answered the ticket (not the first time)
    ADMIN_ANSWERED = "Admin Answered" # in the case of admin answered the ticket ( not the first time)
    USER_CREATED = "User Created" # in the case of user created the ticket ( for the first time)
    ADMIN_NOTIFICATION = "Admin Notification" # in the case of admin clared a notification ( for the first time)
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Empty_Status(Enum):
    EMPTY = "Empty" # in the case of user created the ticket but not message post
    NOT_EMPTY = "Not Empty" # in the case of user created the ticket and has at least one message post
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Seen_Status(Enum):
    SEEN = "Seen"
    UNSEEN = "Unseen"
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class User_Type(Enum):
    CLIENT = "Client"
    ADMINISTRATOR = "Administrator"
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

#################################################### Database Tables ####################################################

class Plan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False)
    modify_time_slot = models.DateTimeField(blank=True, null=True, default=None)
    description = models.CharField(max_length=50, blank=True)
    count = models.IntegerField(blank=False, default=0)
    price = models.FloatField(blank=False, default=0)
    discount = models.IntegerField(blank=False, default=0)
    order = models.IntegerField(blank=False, default=100)
    status = models.CharField(max_length=50, choices=Plan_Status.choices())
    tag = models.CharField(max_length=50, blank=True)

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=50, choices=Payment_Status.choices())
    payment_type = models.CharField(max_length=50, choices=Payment_Type.choices())
    payment_time_slot = models.DateTimeField(blank=True, null=True, default=None)
    price = models.FloatField(blank=False, default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='payment', default = None)
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name='payment')
    paying_id = models.CharField(max_length=10000, blank=True)

class Bulk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bulk')
    bulk_start_time_slot = models.DateTimeField(blank=False, null=False)
    bulk_end_time_slot = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=10000, blank=True)
    status = models.CharField(max_length=50, choices=Bulk_Status.choices())
    request_type = models.CharField(max_length=50, choices=Request_Type.choices())
    total_count = models.IntegerField(blank=False, default=0)
    passed_count = models.IntegerField(blank=False, default=0)

class Request(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='request', null=True)
    request_time_slot = models.DateTimeField(blank=False, null=False)
    result_time_slot = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=Request_Status.choices())
    # process_status = models.CharField(max_length=50, choices=Request_Process_Status.choices(), blank=True, null=True)
    run_type = models.CharField(max_length=50, choices=Request_Run_Type.choices())
    request_type = models.CharField(max_length=50, choices=Request_Type.choices())
    query = models.CharField(max_length=5000, blank=True)
    result = models.CharField(max_length=5000, blank=True, null=True)
    bulk = models.ForeignKey(
        Bulk, on_delete=models.CASCADE, related_name='request', null=True)
    order = models.IntegerField(blank=True, null=True, default=0)

class Request_Bulk_Process(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    process_status = models.CharField(max_length=50, choices=Request_Process_Status.choices(), blank=True, null=True)
    query = models.CharField(max_length=5000, blank=True)
    request_type = models.CharField(max_length=50, choices=Request_Type.choices())
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, related_name='request', null=False)

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ticket')
    title = models.CharField(max_length=10000, blank=True)
    status = models.CharField(max_length=50, choices=Ticket_Status.choices())
    empty_status = models.CharField(max_length=50, choices=Empty_Status.choices())
    client_seen_status = models.CharField(max_length=50, choices=Seen_Status.choices())
    admin_seen_status = models.CharField(max_length=50, choices=Seen_Status.choices())
    question_time_slot = models.DateTimeField(blank=False, null=False)
    answer_time_slot = models.DateTimeField(blank=True, null=True)
    message_count = models.IntegerField(blank=True, default=0)

class Ticket_Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ticket_message')
    body = models.CharField(max_length=10000, blank=True)
    seen_status = models.CharField(max_length=50, choices=Seen_Status.choices())
    user_type = models.CharField(max_length=50, choices=User_Type.choices())
    time_slot = models.DateTimeField(blank=False, null=False)
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='ticket')

class User_Log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_log')
    activity = models.CharField(max_length=10000, blank=True)
    time_slot = models.DateTimeField(blank=False, null=False)

class User_Other_Fields(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    remain_count = models.IntegerField(blank=True, default=50)
    expired_date = models.DateTimeField(blank=True, null=True)
    promotion_code_used = models.BooleanField(blank=True, null=True, default=False)
    user_key = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='other_fields', default = None)
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name='other_fields', default = None)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=1500, null=False)
    image_name = models.CharField(max_length=1500, null=False)
    # image = models.ImageField(upload_to='static/assets/img/blog/')   # i m facing problem for this field
    time_slot = models.DateTimeField(blank=False, null=False)
    status = models.CharField(max_length=50, choices=Post_Status.choices())

class Post_Paragraph(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.CharField(max_length=10000, blank=True)
    time_slot = models.DateTimeField(blank=False, null=False)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post')

class Discount_Code(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time_slot = models.DateTimeField(blank=True, null=True, default=None)
    code = models.CharField(max_length=50, default='', blank=True)
    value = models.FloatField(blank=False, default=0)
    status = models.CharField(max_length=50, choices=Plan_Status.choices())