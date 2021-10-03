# Generated by Django 3.2.7 on 2021-10-03 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='team',
            name='team_id',
        ),
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.PositiveIntegerField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveSmallIntegerField()),
                ('rebounds', models.PositiveSmallIntegerField()),
                ('assists', models.PositiveSmallIntegerField()),
                ('blocks', models.PositiveSmallIntegerField()),
                ('free_throws_attempts', models.PositiveSmallIntegerField()),
                ('free_throws_made', models.PositiveSmallIntegerField()),
                ('free_throws_percent', models.FloatField()),
                ('field_goals_attempts', models.PositiveSmallIntegerField()),
                ('field_goals_made', models.PositiveSmallIntegerField()),
                ('field_goals_percent', models.FloatField()),
                ('games', models.ManyToManyField(to='analyser.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyser.player')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyser.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_team', to='analyser.team'),
        ),
        migrations.AddField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_team', to='analyser.team'),
        ),
    ]