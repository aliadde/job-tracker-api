from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import Companies

class CompanyRepository:
    
    async def create(self, db: AsyncSession, company: Companies):
        db.add(company)
        await db.commit()
        await db.refresh(company)
        return company
    
    async def delete(self, db: AsyncSession, company: Companies):
            await db.delete(company)
            await db.commit()