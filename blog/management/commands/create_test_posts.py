from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Category


class Command(BaseCommand):
    help = 'Create test blog posts'

    def handle(self, *args, **options):
        try:
            # Get admin user
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                self.stdout.write(self.style.ERROR('No admin user found'))
                return

            # Create category
            category, created = Category.objects.get_or_create(
                name='Football',
                defaults={'description': 'Football match previews and analysis'}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

            # Create test post
            post, created = Post.objects.get_or_create(
                slug='barcelona-vs-getafe-match-preview',
                defaults={
                    'title': 'Barcelona vs Getafe Match Preview',
                    'excerpt': 'A comprehensive preview of the upcoming Barcelona vs Getafe match.',
                    'content': '''
                    <h2>Match Overview</h2>
                    <p>Barcelona will face Getafe in what promises to be an exciting La Liga encounter. This match preview covers everything you need to know about the upcoming fixture.</p>
                    
                    <h3>Team Form</h3>
                    <p>Barcelona has been in excellent form this season, showcasing their attacking prowess and tactical discipline under their current management.</p>
                    
                    <h3>Key Players to Watch</h3>
                    <ul>
                        <li>Barcelona's attacking trio</li>
                        <li>Getafe's defensive stalwarts</li>
                        <li>Midfield battle will be crucial</li>
                    </ul>
                    
                    <h3>Prediction</h3>
                    <p>This should be an interesting tactical battle between Barcelona's attacking flair and Getafe's defensive organization.</p>
                    ''',
                    'author': admin_user,
                    'category': category,
                    'status': 'published',
                    'meta_description': 'Barcelona vs Getafe match preview and analysis'
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created blog post: {post.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Blog post already exists: {post.title}'))
                
            self.stdout.write(self.style.SUCCESS(f'Post URL: /blog/post/{post.slug}/'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating test posts: {e}'))