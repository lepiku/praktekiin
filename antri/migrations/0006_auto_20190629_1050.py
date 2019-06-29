# Generated by Django 2.1.7 on 2019-06-29 03:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antri', '0005_auto_20190628_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kepalakeluarga',
            name='alamat',
            field=models.TextField(validators=[django.core.validators.RegexValidator(inverse_match=True, message='Alamat tidak boleh mengandung simbol yang aneh.', regex='[`~!@#$%^&*()_+=\\[\\]{}\\\\|;:"<>/?]')]),
        ),
    ]
