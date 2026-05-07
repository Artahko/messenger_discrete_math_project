from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0005_message_file_message_file_name_message_file_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.CharField(max_length=32, default='bob'),
        ),
    ]
