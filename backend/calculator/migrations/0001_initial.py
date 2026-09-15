from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Calculation",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("device_id", models.UUIDField(db_index=True)),
                ("expression", models.TextField()),
                ("normalized_expression", models.TextField(blank=True)),
                ("result", models.TextField()),
                ("angle_mode", models.CharField(choices=[("deg", "Degrees"), ("rad", "Radians")], default="deg", max_length=3)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(
            model_name="calculation",
            index=models.Index(fields=["device_id", "-created_at"], name="calculator__device__c758ff_idx"),
        ),
    ]
