from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup the Site instance with the correct domain and name'

    def handle(self, *args, **options):
        site_id = getattr(settings, 'SITE_ID', 1)
        domain = getattr(settings, 'SITE_DOMAIN', 'muhammadilyas.tech')
        name = getattr(settings, 'SITE_NAME', 'Muhammad Ilyas')
        
        self.stdout.write(f'Setting up Site with ID={site_id}, domain={domain}, name={name}')
        
        try:
            # Try to get existing site
            site = Site.objects.get(id=site_id)
            site.domain = domain
            site.name = name
            site.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Updated Site {site_id}: {domain}'))
        except Site.DoesNotExist:
            # Create new site
            site = Site.objects.create(
                id=site_id,
                domain=domain,
                name=name
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Created Site {site_id}: {domain}'))
        
        # Show all sites for verification
        all_sites = Site.objects.all()
        self.stdout.write('\nCurrent Sites in database:')
        for s in all_sites:
            self.stdout.write(f'  - ID: {s.id}, Domain: {s.domain}, Name: {s.name}')
