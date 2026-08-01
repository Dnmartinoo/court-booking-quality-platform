from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Venue(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="venues",
    )
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Court(models.Model):
    class CourtType(models.TextChoices):
        FOOTBALL_5 = "F5", "Futbol 5"
        FOOTBALL_7 = "F7", "Futbol 7"
        FOOTBALL_8 = "F8", "Futbol 8"
        FOOTBALL_9 = "F9", "Futbol 9"
        FOOTBALL_11 = "F11", "Futbol 11"

    venue = models.ForeignKey(
        Venue,
        on_delete=models.PROTECT,
        related_name="courts",
    )
    name = models.CharField(max_length=100)
    court_type = models.CharField(
        max_length=3,
        choices=CourtType.choices,
    )
    price_per_slot = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    active = models.BooleanField(default=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["venue__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["venue", "name"],
                name="unique_court_name_per_venue",
            ),
        ]

    def clean(self) -> None:
        super().clean()

        if self.opening_time and self.closing_time:
            if self.opening_time >= self.closing_time:
                raise ValidationError(
                    {
                        "closing_time": (
                            "Closing time must be later than opening time."
                        )
                    }
                )

        if self.price_per_slot is not None and self.price_per_slot <= 0:
            raise ValidationError(
                {
                    "price_per_slot": (
                        "Price per slot must be greater than zero."
                    )
                }
            )

    def __str__(self) -> str:
        return f"{self.venue.name} - {self.name}"


class MaintenanceBlock(models.Model):
    court = models.ForeignKey(
        Court,
        on_delete=models.PROTECT,
        related_name="maintenance_blocks",
    )
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["starts_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(ends_at__gt=models.F("starts_at")),
                name="maintenance_end_after_start",
            ),
        ]

    def clean(self) -> None:
        super().clean()

        if self.starts_at and self.ends_at:
            if self.starts_at >= self.ends_at:
                raise ValidationError(
                    {
                        "ends_at": (
                            "End date and time must be later than start date and time."
                        )
                    }
                )

    def __str__(self) -> str:
        return (
            f"{self.court} | "
            f"{self.starts_at:%Y-%m-%d %H:%M} - "
            f"{self.ends_at:%Y-%m-%d %H:%M}"
        )