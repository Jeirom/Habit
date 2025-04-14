from rest_framework.serializers import ValidationError

forbidden_words = ['.com', '.ru', '.eu', '.kz']

def validate_forbidden_words(value):
    if value.lower() != 'youtube.com' and value.lower() in forbidden_words:
        return ValidationError('Использование сторонних ссылок запрещено. Исключение - YouTube')
