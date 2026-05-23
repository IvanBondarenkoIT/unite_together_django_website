from django.db import migrations


# My own migrations fila
def create_document_types(apps, schema_editor):
    TypeOfDocument = apps.get_model('persons', 'TypeOfDocument')
    documents = [
        ('International passport UKR', r'^FF\d{6}$', 'e.g., FF160340'),
        ('Ukrainian passport', r'^[А-Я]{2}\d{6}$', 'e.g., ВА890789 (Ukrainian letters)'),
        ('ID card UKR', r'^\d{9}$', 'e.g., 123456789'),
        ('Birth certificate UKR', r'^\d-КГ\d{6}$|^І-КГ\d{6}$', 'e.g., 1-КГ258881 or І-КГ258881'),
        ('Permanent resident card UKR', r'^IH\d{6}$|^\d{9}$', 'e.g., IH060210 or 123456789'),
        ('Humanitarian status', r'^\d{11}$', 'e.g., 12345678901'),
        ('Temporary residence card GEO', r'^\d{11}$', 'e.g., 12345678901'),
        ('Personal number GEO', r'^\d{11}$', 'e.g., 12345678912'),
        ('Birth certificate GEO', r'^\d{11}$', 'e.g., 12345678901')
    ]
    for name, regex, hint in documents:
        TypeOfDocument.objects.create(name=name, regex=regex, hint=hint)


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0022_typeofdocument_hint'),
    ]

    operations = [
        migrations.RunPython(create_document_types),
    ]
