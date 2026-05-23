from django.db import migrations, models

BATUMI_ADDRESS_UK = "Батумі, вул. 26 Травня, 31"
BATUMI_ADDRESS_EN = "Batumi, 26 May St. 31"
BATUMI_GEOLOCATION = "https://maps.app.goo.gl/d3w5Av5yqw66Z84X6"


def populate_batumi_address(apps, schema_editor):
    Contacts = apps.get_model("about_us", "Contacts")
    Contacts.objects.filter(status=True).update(
        address_batumi=BATUMI_ADDRESS_UK,
        address_batumi_en=BATUMI_ADDRESS_EN,
        geolocation_batumi=BATUMI_GEOLOCATION,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("about_us", "0011_contacts_address_en"),
    ]

    operations = [
        migrations.AddField(
            model_name="contacts",
            name="address_batumi",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="contacts",
            name="address_batumi_en",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddField(
            model_name="contacts",
            name="geolocation_batumi",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.RunPython(populate_batumi_address, migrations.RunPython.noop),
    ]
