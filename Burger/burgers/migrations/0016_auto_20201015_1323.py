# Generated by Django 3.1.2 on 2020-10-15 11:23

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('burgers', '0015_auto_20201015_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customburger',
            name='meats',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(5, 'Beef'), (6, 'Pork'), (1, 'Grass'), (7, 'Urf'), (8, 'Nugget')], max_length=9),
        ),
    ]
