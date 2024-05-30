# Generated by Django 4.2.13 on 2024-05-30 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0004_alter_polisai_draudimo_suma_alter_polisai_iskaita"),
    ]

    operations = [
        migrations.AddField(
            model_name="klientai",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="polisai",
            name="iskaita",
            field=models.FloatField(),
        ),
    ]
