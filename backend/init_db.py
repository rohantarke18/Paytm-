from .database import engine, Base
from .models import Transaction

Base.metadata.create_all(bind=engine)

print("Database created successfully!")