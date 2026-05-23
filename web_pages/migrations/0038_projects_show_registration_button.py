from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web_pages", "0037_news_url_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="projects",
            name="show_registration_button",
            field=models.BooleanField(
                default=True,
                help_text="Show the registration button on the project page.",
            ),
        ),
    ]
