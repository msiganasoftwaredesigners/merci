from django.db import migrations, models


class Migration(migrations.Migration):
    """Make email, language and timeline optional and add the retainer / NGO service choices.

    Only name, phone, service and a short description are required now, so enquiring takes under a minute.
    """

    dependencies = [
        ('merci', '0003_mercitestimonial_merciphoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merciinquiry',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='merciinquiry',
            name='language',
            field=models.CharField(blank=True, choices=[('amharic', 'Amharic'), ('oromo', 'Afaan Oromoo'), ('tigrinya', 'Tigrinya'), ('somali', 'Somali'), ('afar', 'Afar'), ('english', 'English'), ('french', 'French'), ('arabic', 'Arabic'), ('other', 'Other (tell us in the description)')], max_length=20, verbose_name='Preferred production language'),
        ),
        migrations.AlterField(
            model_name='merciinquiry',
            name='timeline',
            field=models.CharField(blank=True, choices=[('asap', 'As soon as possible'), ('2_weeks', 'Within 2 weeks'), ('1_month', 'Within 1 month'), ('1_3_months', '1 to 3 months'), ('flexible', 'Flexible')], max_length=20),
        ),
        migrations.AlterField(
            model_name='merciinquiry',
            name='service',
            field=models.CharField(choices=[('video', 'Video production'), ('retainer', 'Monthly content package'), ('ngo', 'NGO documentary or campaign'), ('photography', 'Photography'), ('studio', 'Studio production'), ('documentary', 'Documentary production'), ('multilingual', 'Multilingual content'), ('hosting', 'Video hosting and presentation'), ('package', 'Complete production package')], max_length=20),
        ),
    ]
