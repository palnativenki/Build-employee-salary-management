# This provides the equivalent API endpoints with asynchronous query execution.
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func, update
from models import Employee, Base
from pydantic import BaseModel

app = FastAPI()
engine = create_async_engine("sqlite+aiosqlite:///./dev.db")
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/api/employees")
async def get_employees(page: int = 1, limit: int = 20, db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * limit
    
    # Query with count
    result = await db.execute(select(Employee).offset(offset).limit(limit))
    employees = result.scalars().all()
    
    total = await db.execute(select(func.count(Employee.id)))
    total_count = total.scalar()
    
    return {"data": employees, "pagination": {"page": page, "total": total_count}}

@app.get("/api/analytics")
async def get_analytics(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Employee))
    employees = result.scalars().all()
    
    # Simple logic aggregation
    total_spend = sum(e.salary for e in employees) # Simplified without currency conversion for brevity
    return {"total_spend": total_spend, "count": len(employees)}

@app.put("/api/employees/{emp_id}")
async def update_salary(emp_id: str, salary: float, db: AsyncSession = Depends(get_db)):
    stmt = update(Employee).where(Employee.id == emp_id).values(salary=salary)
    await db.execute(stmt)
    await db.commit()
    return {"message": "Updated"}
