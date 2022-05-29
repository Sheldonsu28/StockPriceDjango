# Generated by Django 3.2.13 on 2022-05-29 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=5)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='symbols', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'symbol')},
            },
        ),
    ]
