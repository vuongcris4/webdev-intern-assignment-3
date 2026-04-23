from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StudentScore",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sbd", models.CharField(db_index=True, max_length=20, unique=True)),
                ("toan", models.FloatField(blank=True, null=True)),
                ("ngu_van", models.FloatField(blank=True, null=True)),
                ("ngoai_ngu", models.FloatField(blank=True, null=True)),
                ("vat_li", models.FloatField(blank=True, null=True)),
                ("hoa_hoc", models.FloatField(blank=True, null=True)),
                ("sinh_hoc", models.FloatField(blank=True, null=True)),
                ("lich_su", models.FloatField(blank=True, null=True)),
                ("dia_li", models.FloatField(blank=True, null=True)),
                ("gdcd", models.FloatField(blank=True, null=True)),
                ("ma_ngoai_ngu", models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={"db_table": "student_scores"},
        ),
    ]
