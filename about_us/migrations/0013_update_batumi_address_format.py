from django.db import migrations

BATUMI_ADDRESS_UK = "Батумі, вул. 26 Травня, 31"
BATUMI_ADDRESS_EN = "Batumi, 26 May St. 31"


def update_batumi_address_format(apps, schema_editor):
    Contacts = apps.get_model("about_us", "Contacts")
    Contacts.objects.filter(status=True).update(
        address_batumi=BATUMI_ADDRESS_UK,
        address_batumi_en=BATUMI_ADDRESS_EN,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("about_us", "0012_contacts_batumi_address"),
    ]

    operations = [
        migrations.RunPython(update_batumi_address_format, migrations.RunPython.noop),
    ]
