# tickets/models.py
from django.db import models
from resources.user.models import User
from resources.entity.models import EntityRelatedModel


class Ticket(EntityRelatedModel):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    SENTIMENT_CHOICES = [
        ("positive", "Positive"),
        ("neutral", "Neutral"),
        ("negative", "Negative"),
    ]

    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default="open")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES,
                                default="low")
    category = models.CharField(max_length=50, blank=True, null=True)
    sentiment = models.CharField(
        max_length=10, choices=SENTIMENT_CHOICES, blank=True, null=True
    )
    viewed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="assigned_tickets",
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tickets"
    )
    comments = models.JSONField(blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)
    ai_assigned = models.BooleanField(default=False)
    resolution = models.TextField(blank=True, null=True)
    es_ticket_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = "supportaura_ticket"
