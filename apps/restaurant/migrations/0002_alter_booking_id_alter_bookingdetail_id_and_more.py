# Generated by Django 5.0.3 on 2024-05-21 06:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bookingdetail',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='categorysub',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='food',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='foodsub',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='menu',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='mytable',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='translation',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100, primary_key=True, serialize=False),
        ),
    ]
