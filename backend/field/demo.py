"""Deterministic presentation fixtures. Never used unless DEMO_MODE is enabled."""
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import FieldData


def satellite_data(user=None, field_id=None, field_instance=None, **kwargs):
    field = field_instance
    if field is not None and user is not None and field.user_id != user.pk:
        return {'error': 'Field not found'}
    if field is None:
        if user is None:
            return {'error': 'User required'}
        field = (get_object_or_404(FieldData, id=field_id, user=user) if field_id
                 else FieldData.objects.filter(user=user).first())
    if field is None:
        return {'error': 'No fields found'}
    today = timezone.localdate()
    offset = (field.pk % 3) * 0.025
    ndvi = [round(0.48 + i * 0.021 + offset, 3) for i in range(12)]
    return {
        'source': 'demo', 'NDVI': ndvi[-1], 'EVI': 0.52, 'SAVI': 0.61,
        'crop_type_class': 40, 'rainfall_mm': 3.8, 'temperature_K': 299.15,
        'soil_moisture': 0.31,
        'ndvi_time_series': [{'date': (today - timedelta(days=(11-i)*7)).isoformat(), 'NDVI': n}
                             for i, n in enumerate(ndvi)],
        'ndwi_time_series': [{'date': (today - timedelta(days=(11-i)*7)).isoformat(),
                              'NDWI': [0.24, 0.12, -0.08, -0.14, 0.22, 0.16][i % 6]}
                             for i in range(12)],
    }


def weather_data():
    now = timezone.now()
    def entry(i):
        return {'dt': int((now + timedelta(hours=i*3)).timestamp()),
                'main': {'temp': 26 + (i % 4), 'humidity': 65},
                'weather': [{'main': 'Clouds', 'description': 'scattered clouds', 'icon': '03d'}],
                'wind': {'speed': 2.5}, 'pop': 0.1}
    return {'source': 'demo', 'current': entry(0), 'forecast': [entry(i) for i in range(1, 9)]}


def chat_reply(question):
    q = question.lower()
    if any(word in q for word in ['water', 'weather', 'irrigat']):
        advice = 'Check soil moisture before irrigating and inspect drainage after rain. Schedule watering in the early morning and adjust to the crop stage and local forecast.'
    elif any(word in q for word in ['fertiliz', 'soil', 'nutrient']):
        advice = 'Use a soil test to choose nutrient inputs. Record applications in the field log and follow locally recommended crop-specific doses.'
    else:
        advice = 'Inspect leaves and roots regularly and record changes in the field log. Compare vegetation trends with field observations; consult a local agronomist before treatment.'
    return 'Presentation demo — preset guidance, not a live AI response. ' + advice
