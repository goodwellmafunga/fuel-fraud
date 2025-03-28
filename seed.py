# seed.py

from app import create_app, db
from app.models.user import User
from app.models.station import Station
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# Drop all and recreate (for fresh start - use with care)
db.drop_all()
db.create_all()

# Add test users
admin = User(
    username='admin',
    email='admin@example.com',
    password_hash=generate_password_hash('admin123'),
    role='admin'
)

manager = User(
    username='manager1',
    email='manager1@example.com',
    password_hash=generate_password_hash('manager123'),
    role='manager'
)

attendant = User(
    username='attendant1',
    email='attendant1@example.com',
    password_hash=generate_password_hash('attendant123'),
    role='attendant'
)

# Add test stations
station1 = Station(
    name="Apex Harare Fuel Station",
    location="Harare CBD",
    current_stock=20000,
    price_per_liter=1.58
)

station2 = Station(
    name="Apex Bulawayo Depot",
    location="Bulawayo Industrial Area",
    current_stock=15000,
    price_per_liter=1.62
)

# Commit to DB
db.session.add_all([admin, manager, attendant, station1, station2])
db.session.commit()

print("✅ Seed complete: Users and stations added.")
