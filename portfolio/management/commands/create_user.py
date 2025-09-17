from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from getpass import getpass

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a new user interactively'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the new user')
        parser.add_argument('--email', type=str, help='Email for the new user')
        parser.add_argument('--password', type=str, help='Password for the new user')
        parser.add_argument('--superuser', action='store_true', help='Create as superuser')
        parser.add_argument('--staff', action='store_true', help='Create as staff user')

    def handle(self, *args, **options):
        # Get username
        username = options.get('username')
        if not username:
            username = input('Username: ')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.ERROR(f'User "{username}" already exists!')
            )
            return

        # Get email
        email = options.get('email')
        if not email:
            email = input('Email address: ')

        # Get password
        password = options.get('password')
        if not password:
            password = getpass('Password: ')
            password_confirm = getpass('Password (again): ')
            if password != password_confirm:
                self.stdout.write(
                    self.style.ERROR('Passwords do not match!')
                )
                return

        # Create user
        try:
            if options.get('superuser'):
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                user_type = "superuser"
            elif options.get('staff'):
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.is_staff = True
                user.save()
                user_type = "staff user"
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user_type = "regular user"

            self.stdout.write(
                self.style.SUCCESS(f'{user_type.title()} "{username}" created successfully!')
            )
            self.stdout.write(f'Email: {email}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating user: {e}')
            )