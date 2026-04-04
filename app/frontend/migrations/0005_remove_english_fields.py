from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_streamline_public_site'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exhibit',
            old_name='excerpt_it',
            new_name='excerpt',
        ),
        migrations.RenameField(
            model_name='exhibit',
            old_name='description_it',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='exhibit',
            name='excerpt_en',
        ),
        migrations.RemoveField(
            model_name='exhibit',
            name='description_en',
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='excerpt',
            field=models.CharField(blank=True, default='', help_text='breve descrizione della mostra', max_length=255, null=True, verbose_name='excerpt'),
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='description',
            field=models.TextField(help_text='descrizione completa della mostra', verbose_name='description'),
        ),
        migrations.AlterModelOptions(
            name='exhibit',
            options={
                'db_table': 'exhibit',
                'ordering': ['-ended_at', '-begun_at', '-id'],
                'verbose_name': 'exhibit',
                'verbose_name_plural': 'exhibits',
            },
        ),
    ]
