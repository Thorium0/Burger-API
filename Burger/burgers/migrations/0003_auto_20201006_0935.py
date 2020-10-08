# Generated by Django 3.1.2 on 2020-10-06 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('burgers', '0002_auto_20201005_1048'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='customburger',
            name='image',
            field=models.ImageField(default='default-burger.png', upload_to='burger_pics/'),
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='burgers.featurecategory')),
            ],
        ),
        migrations.AddField(
            model_name='customburger',
            name='selectBox',
            field=models.ManyToManyField(blank=True, to='burgers.Feature'),
        ),
    ]
