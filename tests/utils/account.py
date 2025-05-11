import random
import string
from typing import Optional
from sqlalchemy.orm import Session
from app.models.account import Account

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))

def random_url() -> str:
    return f"https://{random_lower_string()}.com"

def create_random_account(
    db: Session,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    website_url: Optional[str] = None,
    industry: Optional[str] = None,
    employee_count: Optional[int] = None,
    annual_revenue: Optional[int] = None,
    is_active: bool = True,
    owner_id: Optional[int] = None,
    creator_id: Optional[int] = None,
    updater_id: Optional[int] = None,
) -> Account:
    if name is None:
        name = random_lower_string()
    if description is None:
        description = random_lower_string()
    if website_url is None:
        website_url = random_url()
    if industry is None:
        industry = random_lower_string()
    if employee_count is None:
        employee_count = random.randint(1, 1000)
    if annual_revenue is None:
        annual_revenue = random.randint(10000, 10000000)
    
    account = Account(
        name=name,
        description=description,
        website_url=website_url,
        industry=industry,
        employee_count=employee_count,
        annual_revenue=annual_revenue,
        is_active=is_active,
        owner_id=owner_id,
        creator_id=creator_id,
        updater_id=updater_id
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account 