from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser automatically for production deployment'

    def handle(self, *args, **options):
        # Get credentials from environment variables or use defaults
        username = config('ADMIN_USERNAME', default='admin')
        email = config('ADMIN_EMAIL', default='admin@example.com')
        password = config('ADMIN_PASSWORD', default='admin123')

        # Create or get the admin user
        try:
            admin_user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            if created:
                admin_user.set_password(password)
                admin_user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Superuser "{username}" created successfully!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Superuser "{username}" already exists.')
                )
            
            # Create or get the ilyas user as backup
            ilyas_user, created = User.objects.get_or_create(
                username='ilyas',
                defaults={
                    'email': 'ilyaskhanqwer0088@gmail.com',
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            if created:
                ilyas_user.set_password('Kkhan123')
                ilyas_user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Backup superuser "ilyas" created successfully!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Backup superuser "ilyas" already exists.')
                )
                
            self.stdout.write(
                self.style.SUCCESS('User creation process completed!')
            )
            self.stdout.write(
                self.style.WARNING('Login credentials for production:')
            )
            self.stdout.write(f'  Username: {username} | Password: {password}')
            self.stdout.write(f'  Username: ilyas | Password: Kkhan123')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )