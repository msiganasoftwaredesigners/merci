from django.db import migrations, models


class Migration(migrations.Migration):
    """Add the private-event service choice (birthdays, weddings, graduations)."""

    dependencies = [
        ('merci', '0004_inquiry_optional_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merciinquiry',
            name='service',
            field=models.CharField(choices=[('video', 'Video production'), ('retainer', 'Monthly content package'), ('ngo', 'NGO documentary or campaign'), ('event', 'Birthday, wedding or private event'), ('photography', 'Photography'), ('studio', 'Studio production'), ('documentary', 'Documentary production'), ('multilingual', 'Multilingual content'), ('hosting', 'Video hosting and presentation'), ('package', 'Complete production package')], max_length=20),
        ),
    ]
