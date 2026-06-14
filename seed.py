# This script replicates the logic used in the previous step, ensuring the same 10,000-record dataset.
import asyncio
import random
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base, Employee

DATABASE_URL = "sqlite+aiosqlite:///./dev.db"

async def seed_data():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    DEPARTMENTS = ['Engineering', 'Product', 'Sales', 'Marketing', 'HR', 'Finance', 'Legal']
    COUNTRIES = [
        {'name': 'United States', 'currency': 'USD', 'min': 60000, 'max': 180000},
        {'name': 'United Kingdom', 'currency': 'GBP', 'min': 45000, 'max': 120000},
    ] # Add others as needed
    
    FIRST_NAMES = ['James', 'Mary', 'John', 'Patricia']
    LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown']

    async with async_session() as session:
        print("Seeding 10,000 employees...")
        employees = []
        for i in range(10000):
            c = random.choice(COUNTRIES)
            emp = Employee(
                id=str(uuid.uuid4()),
                firstName=random.choice(FIRST_NAMES),
                lastName=random.choice(LAST_NAMES),
                email=f"user{i}@acme.com",
                department=random.choice(DEPARTMENTS),
                country=c['name'],
                salary=round(random.uniform(c['min'], c['max']), 2),
                currency=c['currency']
            )
            employees.append(emp)
            
            if len(employees) >= 1000:
                session.add_all(employees)
                await session.commit()
                employees = []
                print(f"Inserted batch...")

    print("Seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_data())
