from rest_framework.serializers import ValidationError

forbidden_words = ['.com', '.ru', '.eu', '.kz']

def validate_time_limit(value):
    if value > 2:
        return ValidationError('Привычка должна быть исполнена в течении 120 секунд и меньше.')

def validate_frequency(frequency):
    if frequency > 7:
        return ValidationError('Периодичность выполнения привычки должна составлять до 7 дней(включительно).')
