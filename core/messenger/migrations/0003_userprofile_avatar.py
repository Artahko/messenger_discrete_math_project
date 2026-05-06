from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0002_userprofile_fields_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.CharField(max_length=32, default='bob'),
        ),
    ]
