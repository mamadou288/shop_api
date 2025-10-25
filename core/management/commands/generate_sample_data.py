"""
Management command to generate sample data for the e-commerce platform.
Usage: python manage.py generate_sample_data
"""
import random
from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from faker import Faker

from products.models import Category, Product, ProductImage
from orders.models import Order, OrderItem, OrderStatus

User = get_user_model()


class Command(BaseCommand):
    help = 'Generate sample data for testing and demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete all existing data before generating new data',
        )
        parser.add_argument(
            '--users',
            type=int,
            default=20,
            help='Number of users to generate (default: 20)',
        )
        parser.add_argument(
            '--products',
            type=int,
            default=80,
            help='Number of products to generate (default: 80)',
        )
        parser.add_argument(
            '--orders',
            type=int,
            default=100,
            help='Number of orders to generate (default: 100)',
        )
        parser.add_argument(
            '--months',
            type=int,
            default=3,
            help='Number of months of historical data (default: 3)',
        )

    def handle(self, *args, **options):
        self.faker = Faker('fr_FR')  # French locale
        Faker.seed(0)  # Reset Faker seed for consistency
        
        # Validate arguments
        if options['users'] < 1 or options['products'] < 1 or options['orders'] < 1:
            self.stdout.write(self.style.ERROR('All counts must be positive numbers'))
            return
        
        if options['months'] < 1:
            self.stdout.write(self.style.ERROR('Months must be at least 1'))
            return
        
        # Flush existing data if requested
        if options['flush']:
            self.stdout.write(self.style.WARNING('Flushing existing data...'))
            self.flush_data()
            self.stdout.write(self.style.SUCCESS('Data flushed'))   
        
        # Generate data
        self.stdout.write(self.style.SUCCESS('Starting data generation...'))
        
        try:
            with transaction.atomic():
                users = self.generate_users(options['users'], options['months'])
                categories = self.generate_categories()
                products = self.generate_products(options['products'], categories, options['months'])
                orders = self.generate_orders(options['orders'], users, products, options['months'])
            
            # Display statistics
            self.stdout.write(self.style.SUCCESS('\nGeneration complete!'))
            self.stdout.write(f'  Users: {len(users)} (1 admin + {len(users)-1} regular)')
            self.stdout.write(f'  Categories: {len(categories)}')
            self.stdout.write(f'  Products: {len(products)}')
            self.stdout.write(f'  Orders: {len(orders)}')
            self.stdout.write(f'  Data period: {options["months"]} months')
            self.stdout.write(self.style.SUCCESS('\nSample data generated successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            raise

    def flush_data(self):
        """Delete all existing data."""
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()

    def generate_users(self, count, months):
        """Generate users with realistic data."""
        self.stdout.write('Generating users...')
        
        users = []
        now = timezone.now()
        
        # Create admin user
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@shop.com',
            password='TestPass123!',
            first_name='Admin',
            last_name='Shop',
            is_admin=True,
        )
        users.append(admin)
        self.stdout.write(f'    ✓ Admin created: {admin.email}')
        
        # Create regular users
        for i in range(count - 1):
            # Random creation date within the months period
            days_ago = random.randint(0, months * 30)
            created_at = now - timedelta(days=days_ago)
            
            email = self.faker.unique.email()
            # Use unique username: prefix + index to avoid collisions
            username = f"{email.split('@')[0]}_{i}"
            user = User.objects.create_user(
                username=username,
                email=email,
                password='TestPass123!',
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                phone=self.faker.phone_number(),
                newsletter_consent=random.choice([True, False]),
                marketing_consent=random.choice([True, False]),
            )
            user.created_at = created_at
            user.save(update_fields=['created_at'])
            users.append(user)
        
        self.stdout.write(self.style.SUCCESS(f'    ✓ Created {count} users'))
        return users

    def generate_categories(self):
        """Generate product categories with hierarchy."""
        self.stdout.write('  📁 Generating categories...')
        
        categories = []
        
        # Root categories with French names
        root_categories_data = [
            {'name': 'Électronique', 'subs': ['Smartphones', 'Ordinateurs', 'Audio']},
            {'name': 'Vêtements', 'subs': ['Homme', 'Femme', 'Enfants']},
            {'name': 'Maison', 'subs': ['Décoration', 'Cuisine', 'Jardin']},
            {'name': 'Sports', 'subs': ['Fitness', 'Running', 'Outdoor']},
            {'name': 'Livres', 'subs': ['Romans', 'Technique', 'Jeunesse']},
        ]
        
        for cat_data in root_categories_data:
            # Create root category
            root = Category.objects.create(
                name=cat_data['name'],
                description=self.faker.text(max_nb_chars=200),
            )
            categories.append(root)
            
            # Create subcategories
            for sub_name in cat_data['subs']:
                sub = Category.objects.create(
                    name=sub_name,
                    parent=root,
                    description=self.faker.text(max_nb_chars=150),
                )
                categories.append(sub)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))
        return categories

    def generate_products(self, count, categories, months):
        """Generate products with realistic data."""
        self.stdout.write('Generating products...')
        
        products = []
        now = timezone.now()
        
        # Product name templates by category
        product_templates = {
            'Smartphones': ['iPhone', 'Samsung Galaxy', 'Google Pixel', 'OnePlus', 'Xiaomi'],
            'Ordinateurs': ['MacBook', 'Dell XPS', 'HP Pavilion', 'Lenovo ThinkPad', 'Asus'],
            'Audio': ['AirPods', 'Sony WH', 'Bose QuietComfort', 'JBL', 'Marshall'],
            'Homme': ['T-shirt', 'Jean', 'Veste', 'Chemise', 'Pull'],
            'Femme': ['Robe', 'Jupe', 'Chemisier', 'Pantalon', 'Pull'],
            'Enfants': ['T-shirt enfant', 'Pantalon enfant', 'Robe enfant', 'Short', 'Sweat'],
            'Décoration': ['Lampe', 'Coussin', 'Tapis', 'Miroir', 'Vase'],
            'Cuisine': ['Set de couteaux', 'Poêle', 'Casserole', 'Mixer', 'Cafetière'],
            'Jardin': ['Tondeuse', 'Barbecue', 'Salon de jardin', 'Parasol', 'Outils'],
            'Fitness': ['Tapis de yoga', 'Haltères', 'Élastiques', 'Kettlebell', 'Banc'],
            'Running': ['Chaussures running', 'Montre GPS', 'Ceinture', 'Brassard', 'Gourde'],
            'Outdoor': ['Tente', 'Sac à dos', 'Sleeping bag', 'Lampe frontale', 'Réchaud'],
            'Romans': ['Roman policier', 'Roman historique', 'Science-fiction', 'Fantasy', 'Thriller'],
            'Technique': ['Python', 'JavaScript', 'Data Science', 'DevOps', 'Machine Learning'],
            'Jeunesse': ['Album illustré', 'Conte', 'BD enfant', 'Livre éducatif', 'Roman ado'],
        }
        
        # Get leaf categories (ones with no children or use all)
        leaf_categories = [c for c in categories if not c.children.exists()]
        
        for i in range(count):
            category = random.choice(leaf_categories)
            
            # Get product template for category
            templates = product_templates.get(category.name, ['Produit'])
            base_name = random.choice(templates)
            
            # Add variant/model + unique ID to avoid slug collisions
            model = random.choice(['Pro', 'Plus', 'Max', 'Air', 'Mini', 'Lite', '2024', 'XL'])
            product_name = f"{base_name} {model} #{i+1}"
            
            # Random price and stock
            price = Decimal(str(round(random.uniform(9.99, 2999.99), 2)))
            stock = random.randint(0, 100)
            
            # Random creation date
            days_ago = random.randint(0, months * 30)
            created_at = now - timedelta(days=days_ago)
            
            product = Product.objects.create(
                name=product_name,
                description=self.faker.text(max_nb_chars=300),
                price=price,
                stock=stock,
                category=category,
                sku=f"SKU-{self.faker.unique.bothify(text='????-#####').upper()}",
            )
            product.created_at = created_at
            product.save(update_fields=['created_at'])
            products.append(product)
            
            # Add 1-3 product images (placeholder URLs)
            num_images = random.randint(1, 3)
            for j in range(num_images):
                ProductImage.objects.create(
                    product=product,
                    image=f"products/placeholder_{random.randint(1, 20)}.jpg",
                    alt_text=f"{product.name} - Image {j+1}",
                    order=j,
                )
        
        self.stdout.write(self.style.SUCCESS(f'Created {count} products with images'))
        return products

    def generate_orders(self, count, users, products, months):
        """Generate orders with realistic status distribution."""
        self.stdout.write('Generating orders...')
        
        orders = []
        now = timezone.now()
        
        # Status distribution
        status_distribution = [
            (OrderStatus.DELIVERED, 50),  # 50%
            (OrderStatus.SHIPPED, 20),     # 20%
            (OrderStatus.CONFIRMED, 15),   # 15%
            (OrderStatus.PENDING, 10),     # 10%
            (OrderStatus.CANCELLED, 5),    # 5%
        ]
        
        # Expand distribution
        status_pool = []
        for status, percentage in status_distribution:
            status_pool.extend([status] * percentage)
        
        # Get products with stock > 0 for orders
        available_products = [p for p in products if p.stock > 0]
        
        if not available_products:
            self.stdout.write(self.style.WARNING('No products with stock, skipping orders'))
            return []
        
        for i in range(count):
            # Random user (skip admin 80% of the time for realism)
            user = random.choice(users[1:]) if random.random() > 0.2 and len(users) > 1 else random.choice(users)
            
            # Random status
            status = random.choice(status_pool)
            
            # Date based on status (older = more likely delivered)
            if status == OrderStatus.DELIVERED:
                days_ago = random.randint(15, months * 30)
            elif status == OrderStatus.SHIPPED:
                days_ago = random.randint(5, 30)
            elif status == OrderStatus.CONFIRMED:
                days_ago = random.randint(2, 10)
            elif status == OrderStatus.PENDING:
                days_ago = random.randint(0, 5)
            else:  # CANCELLED
                days_ago = random.randint(1, months * 30)
            
            order_date = now - timedelta(days=days_ago)
            
            # Create order
            order = Order.objects.create(
                user=user,
                status=status,
                shipping_address=self.faker.street_address(),
                shipping_city=self.faker.city(),
                shipping_postal_code=self.faker.postcode(),
                shipping_country='France',
                notes=self.faker.text(max_nb_chars=100) if random.random() > 0.7 else '',
            )
            order.created_at = order_date
            
            # Set status timestamps
            if status in [OrderStatus.CONFIRMED, OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
                order.confirmed_at = order_date + timedelta(hours=random.randint(1, 24))
            if status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
                order.shipped_at = order.confirmed_at + timedelta(days=random.randint(1, 3))
            if status == OrderStatus.DELIVERED:
                order.delivered_at = order.shipped_at + timedelta(days=random.randint(1, 5))
            if status == OrderStatus.CANCELLED:
                order.cancelled_at = order_date + timedelta(hours=random.randint(1, 48))
            
            order.save()
            
            # Add 1-5 items per order
            num_items = random.randint(1, 5)
            selected_products = random.sample(available_products, min(num_items, len(available_products)))
            
            total = Decimal('0.00')
            
            for product in selected_products:
                quantity = random.randint(1, 3)
                
                # Create order item with snapshot
                item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    product_price=product.price,
                    quantity=quantity,
                )
                total += item.subtotal
                
                # Reduce stock only for non-cancelled orders
                if status != OrderStatus.CANCELLED:
                    if product.stock >= quantity:
                        product.stock -= quantity
                        product.save(update_fields=['stock'])
            
            # Update order total
            order.total_amount = total
            order.save(update_fields=['total_amount', 'created_at', 'confirmed_at', 'shipped_at', 'delivered_at', 'cancelled_at'])
            
            orders.append(order)
        
        self.stdout.write(self.style.SUCCESS(f'Created {count} orders'))
        return orders

