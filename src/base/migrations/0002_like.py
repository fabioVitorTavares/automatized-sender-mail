# Generated by Django 4.2.1 on 2023-06-06 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tutorial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.tutorial')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.usuario')),
            ],
            options={
                'unique_together': {('usuario', 'tutorial')},
            },
        ),
    ]
