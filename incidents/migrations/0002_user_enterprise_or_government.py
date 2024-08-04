# Generated by Django 5.0.7 on 2024-08-04 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='enterprise_or_government',
            field=models.CharField(choices=[('Enterprise', 'Enterprise'), ('Government', 'Government'), ('Individual', 'Individual')], default='Individual', max_length=100),
            preserve_default=False,
        ),
    ]