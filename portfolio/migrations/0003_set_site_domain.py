from django.conf import settings
from django.db import migrations


def set_site_domain(apps, schema_editor):
    Site = apps.get_model('sites', 'Site')
    site_id = getattr(settings, 'SITE_ID', 1)
    domain = getattr(settings, 'SITE_DOMAIN', 'muhammadilyas.tech')
    name = getattr(settings, 'SITE_NAME', 'Portfolio & Blog')

    Site.objects.update_or_create(
        pk=site_id,
        defaults={
            'domain': domain,
            'name': name,
        },
    )


def noop(apps, schema_editor):
    """No-op reverse migration."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_project_featured_image'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(set_site_domain, noop),
    ]
