"""Create repeatable, non-destructive presentation records in a local database."""
from datetime import timedelta
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from field.models import FieldData, FieldLog, FieldAlert
from finance.models import Season, CostEntry, Revenue
from planning.models import SeasonCalendar, InventoryItem


class Command(BaseCommand):
    help = 'Create presentation records (requires DEMO_MODE=True and DEBUG=True)'

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEMO_MODE or not settings.DEBUG:
            raise CommandError('Enable DEMO_MODE=True and DEBUG=True for local sample data.')
        user, created = User.objects.get_or_create(username='demo_farmer', defaults={
            'email': 'demo@example.invalid', 'first_name': 'Demo', 'last_name': 'Farmer'})
        if created:
            user.set_password('DemoFarmer@2026')
            user.save()
        today = timezone.localdate()
        for index, (name, crop) in enumerate([('Ludhiana Wheat Plot', 'Wheat'), ('Ludhiana Rice Plot', 'Rice')]):
            lon, lat = 75.85 + index * 0.004, 30.90
            polygon = {'type': 'Polygon', 'coordinates': [[[lon, lat], [lon+0.002, lat],
                        [lon+0.002, lat+0.001], [lon, lat+0.001], [lon, lat]]]}
            field, _ = FieldData.objects.get_or_create(user=user, name=name,
                                                       defaults={'cropType': crop, 'polygon': polygon})
            season, _ = Season.objects.get_or_create(user=user, field=field, season_type='rabi', year=today.year,
                defaults={'name': f'Presentation season {today.year}', 'start_date': today-timedelta(days=60),
                          'end_date': today+timedelta(days=60), 'crop': crop})
            for category, amount in [('seeds', 6500), ('fertilizer', 4200), ('labor', 9000), ('irrigation', 2300)]:
                CostEntry.objects.get_or_create(user=user, field=field, season=season, description=f'Sample {category}',
                    defaults={'category': category, 'amount': amount, 'date': today-timedelta(days=10)})
            Revenue.objects.get_or_create(user=user, field=field, season=season, notes='Sample sale for presentation',
                defaults={'crop': crop, 'quantity_sold': Decimal('1800'), 'price_per_unit': Decimal('25'),
                          'total_amount': Decimal('45000'), 'buyer': 'Sample local mandi', 'date': today-timedelta(days=2)})
            for days, activity, details in [(14, 'sowing', 'Sample: sowing completed'), (5, 'fertilizer', 'Sample: soil nutrients checked'), (1, 'watering', 'Sample: morning irrigation')]:
                FieldLog.objects.get_or_create(user=user, field=field, details=details,
                    defaults={'date': today-timedelta(days=days), 'activity': activity})
            FieldAlert.objects.get_or_create(user=user, field=field, message='Sample reminder: inspect soil moisture today', defaults={'date': today})
            SeasonCalendar.objects.get_or_create(user=user, field=field, title='Sample: inspect crop health',
                defaults={'activity_type': 'other', 'start_date': today+timedelta(days=1), 'end_date': today+timedelta(days=1)})
        InventoryItem.objects.get_or_create(user=user, name='Sample wheat seeds',
            defaults={'category': 'seeds', 'quantity': 75, 'unit': 'kg', 'reorder_level': 20})
        self.stdout.write(self.style.SUCCESS('Sample records ready. Login: demo_farmer / DemoFarmer@2026'))
        if not created:
            self.stdout.write('Existing account password and records were preserved.')
