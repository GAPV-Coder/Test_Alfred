# Generated by Django 5.2 on 2025-04-28 23:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            ALTER TABLE delivery_service
            ALTER COLUMN estimated_arrival_time
            TYPE timestamp with time zone
            USING to_timestamp(estimated_arrival_time);
            """,
            reverse_sql="""
            ALTER TABLE delivery_service
            ALTER COLUMN estimated_arrival_time
            TYPE double precision
            USING EXTRACT(EPOCH FROM estimated_arrival_time);
            """
        ),
    ]
