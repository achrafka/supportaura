from django.db import models
from django.contrib.auth.models import Permission
from django.urls import reverse


class Entity(models.Model):
    name = models.CharField(max_length=200)
    fake_fqdn = models.CharField(unique=True, max_length=200)
    rank = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    permissions = models.ManyToManyField(
        Permission,
        related_name='entity_permissions_set',
        blank=True,
        help_text="Specific permissions for this entity.",
        verbose_name="entity permissions",
    )
    label = models.CharField(max_length=200)
    addressline = models.CharField(max_length=200, blank=True)
    addressline2 = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=16, default="customer")
    city = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=2, default="FR")
    postalcode = models.CharField(max_length=200, blank=True)
    streetnumber = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "supportaura_entity"
        unique_together = ("label",)


class NtuiGenericModel(models.Model):
    rank = models.IntegerField(blank=True, null=True, verbose_name='Rank')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """
        Returns the absolute URL for the model instance using the reverse()
        method.
        The URL name is dynamically generated based on the model's class name.
        """
        return reverse(self.__class__.__name__.lower() + '_detail',
                       args=[self.entity.pk, self.pk])

    class Meta:
        abstract = True


class EntityRelatedModel(NtuiGenericModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    class DoesNotExist(Exception):
        pass

