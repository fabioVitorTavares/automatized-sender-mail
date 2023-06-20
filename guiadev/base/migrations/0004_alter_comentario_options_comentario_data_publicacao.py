# Generated by Django 4.2.1 on 2023-06-20 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_comentario_options_alter_like_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comentario',
            options={'ordering': ['data_publicacao'], 'verbose_name_plural': 'Comentários'},
        ),
        migrations.AddField(
            model_name='comentario',
            name='data_publicacao',
            field=models.DateTimeField(auto_now_add=True, default='2023-06-20 15:30:45.123456+00:00'),
            preserve_default=False,
        ),
    ]
