# Generated by Django 3.1.2 on 2020-10-09 08:40

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('burgers', '0010_customburger_salads'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customburger',
            name='buns',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Brioche'), (2, 'Sesame seed'), (3, 'Whole wheat'), (4, 'Gluten free'), (5, 'Mixed greens')], max_length=9),
        ),
        migrations.AlterField(
            model_name='customburger',
            name='condiments',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Bacon'), (2, 'Guacamole'), (3, 'Mushrooms'), (4, 'Fried egg'), (5, 'Sausage party'), (6, 'Cheddar cheese'), (7, 'American cheese'), (8, 'Swiss cheese')], max_length=15),
        ),
        migrations.AlterField(
            model_name='customburger',
            name='meats',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(5, 'Beef'), (6, 'Pork'), (1, 'Grass'), (7, 'Urf'), (8, 'Nugget')], max_length=9),
        ),
        migrations.AlterField(
            model_name='customburger',
            name='salads',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Mixed greens'), (2, 'Tomatos'), (3, 'Jalapenos'), (4, 'Pepperoncinis'), (5, 'Red onions'), (6, 'Pickles'), (7, 'Cucumbers'), (8, 'Carrot sticks')], max_length=15),
        ),
    ]
