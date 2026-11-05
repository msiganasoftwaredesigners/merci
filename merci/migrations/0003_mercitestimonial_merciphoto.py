from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merci', '0002_merciproject_custom_mobile_thumbnail_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MerciTestimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('role', models.CharField(blank=True, max_length=120, verbose_name='Role or job title')),
                ('organization', models.CharField(blank=True, max_length=160)),
                ('client_type', models.CharField(choices=[('company', 'Company'), ('ngo', 'NGO / institution'), ('individual', 'Individual / personal brand')], default='company', max_length=12)),
                ('quote', models.TextField(help_text='What the client said, in their own words. Keep it under about 400 characters.')),
                ('photo', models.ImageField(blank=True, help_text='Optional. A square portrait or the client logo.', upload_to='merci/testimonials/')),
                ('video_url', models.URLField(blank=True, help_text="Optional. If added, visitors can play the client's video testimonial.", verbose_name='YouTube link (video testimonial)')),
                ('is_published', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Merci testimonial',
                'verbose_name_plural': 'Merci testimonials',
                'ordering': ['order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MerciPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('category', models.CharField(choices=[('corporate', 'Corporate'), ('portrait', 'Portraits'), ('product', 'Product'), ('event', 'Events'), ('documentary', 'Documentary'), ('behind', 'Behind the scenes')], default='corporate', max_length=12)),
                ('image', models.ImageField(help_text='Landscape or portrait both work. Keep the file under 1 MB (about 1600 px on the long side) so the page stays fast.', upload_to='merci/photos/')),
                ('alt_text', models.CharField(blank=True, help_text='Describe the photo in a few words. Helps Google Images and screen readers. Defaults to the title.', max_length=200)),
                ('is_published', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0, help_text='Lower numbers appear first.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Merci photo',
                'verbose_name_plural': 'Merci photos',
                'ordering': ['order', '-created_at'],
            },
        ),
    ]
