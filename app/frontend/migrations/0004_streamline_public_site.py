from django.db import migrations, models


def copy_exhibit_authors_to_text(apps, schema_editor):
    Exhibit = apps.get_model('frontend', 'Exhibit')

    for exhibit in Exhibit.objects.all():
        names = []
        for author in exhibit.authors.all().order_by('last_name', 'first_name'):
            first_name = (author.first_name or '').strip()
            last_name = (author.last_name or '').strip()
            if first_name and last_name:
                names.append('%s %s' % (first_name.capitalize(), last_name.capitalize()))
            elif last_name:
                names.append(last_name.capitalize())
            elif first_name:
                names.append(first_name.capitalize())

        Exhibit.objects.filter(pk=exhibit.pk).update(
            authors_text=', '.join(names),
        )


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_auto_20260326_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibit',
            name='authors_text',
            field=models.TextField(blank=True, default='', help_text='autori della mostra', verbose_name='authors'),
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='description_en',
            field=models.TextField(help_text='descrizione completa della mostra(inglese)', verbose_name='description_en'),
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='description_it',
            field=models.TextField(help_text='descrizione completa della mostra', verbose_name='description_it'),
        ),
        migrations.RunPython(copy_exhibit_authors_to_text, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='exhibit',
            name='authors',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.RenameField(
            model_name='exhibit',
            old_name='authors_text',
            new_name='authors',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.DeleteModel(
            name='ResumeEvent',
        ),
        migrations.DeleteModel(
            name='ResumeSection',
        ),
        migrations.DeleteModel(
            name='Resume',
        ),
        migrations.DeleteModel(
            name='BoardItem',
        ),
    ]
