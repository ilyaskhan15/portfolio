# Generated migration to set up Site domain

from django.db import migrations


def set_site_domain(apps, schema_editor):
    """
    Set the domain and name for the Site instance.
    This migration ensures the Site entry exists and is correctly configured.
    """
    Site = apps.get_model('sites', 'Site')
    
    # Delete any existing sites first to avoid unique constraint issues
    Site.objects.all().delete()
    
    # Create the site with ID=1 (matches SITE_ID in settings)
    Site.objects.create(
        id=1,
        domain='muhammadilyas.tech',
        name='Muhammad Ilyas'
    )


def revert_site_domain(apps, schema_editor):
    """
    Revert to default example.com domain.
    """
    Site = apps.get_model('sites', 'Site')
    Site.objects.filter(id=1).update(
        domain='example.com',
        name='example.com'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(set_site_domain, revert_site_domain),
    ]
