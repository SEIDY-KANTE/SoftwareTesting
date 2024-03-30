# Generated by Django 5.0.3 on 2024-03-30 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('ClassName', models.CharField(max_length=70)),
                ('JavaDocLines', models.IntegerField()),
                ('OtherComments', models.IntegerField()),
                ('CodeLines', models.IntegerField()),
                ('Loc', models.IntegerField()),
                ('FunctionLines', models.IntegerField()),
                ('CommentDeviation', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
