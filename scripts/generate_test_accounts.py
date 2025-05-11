#!/usr/bin/env python3
import sys
import os
import random
from datetime import datetime
from typing import List, Dict, Any

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.account import Account
from app.core.config import settings

# Sample data for generating realistic test accounts
INDUSTRIES = [
    "Technology",
    "Healthcare",
    "Finance",
    "Manufacturing",
    "Retail",
    "Education",
    "Real Estate",
    "Energy",
    "Transportation",
    "Media & Entertainment"
]

COMPANY_SUFFIXES = [
    "Inc.",
    "LLC",
    "Corp.",
    "Ltd.",
    "Group",
    "International",
    "Systems",
    "Solutions",
    "Technologies",
    "Enterprises"
]

def generate_company_name() -> str:
    """Generate a realistic company name."""
    prefixes = [
        "Global", "Advanced", "Smart", "Future", "Digital", "Innovative",
        "United", "Premier", "Elite", "Prime", "Core", "Vertex", "Nexus",
        "Quantum", "Alpha", "Beta", "Delta", "Omega", "Sigma", "Gamma"
    ]
    industries = [
        "Tech", "Systems", "Solutions", "Services", "Industries", "Group",
        "Enterprises", "Holdings", "Partners", "Ventures", "Capital"
    ]
    
    return f"{random.choice(prefixes)} {random.choice(industries)} {random.choice(COMPANY_SUFFIXES)}"

def generate_website_url(company_name: str) -> str:
    """Generate a website URL based on company name."""
    base_name = company_name.lower().replace(" ", "").replace(".", "").replace(",", "")
    return f"https://www.{base_name}.com"

def generate_account_data() -> Dict[str, Any]:
    """Generate a single account's data."""
    company_name = generate_company_name()
    return {
        "name": company_name,
        "description": f"A leading company in {random.choice(INDUSTRIES)} industry, providing innovative solutions.",
        "website_url": generate_website_url(company_name),
        "industry": random.choice(INDUSTRIES),
        "employee_count": random.randint(10, 10000),
        "annual_revenue": random.randint(100000, 1000000000),
        "is_active": random.choice([True, True, True, False]),  # 75% chance of being active
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "touched_at": datetime.utcnow()
    }

def create_test_accounts(db: Session, num_accounts: int = 50) -> List[Account]:
    """Create test accounts in the database."""
    accounts = []
    for _ in range(num_accounts):
        account_data = generate_account_data()
        account = Account(**account_data)
        db.add(account)
        accounts.append(account)
    
    db.commit()
    for account in accounts:
        db.refresh(account)
    
    return accounts

def main():
    """Main function to generate test accounts."""
    print("Starting test account generation...")
    
    db = SessionLocal()
    try:
        # Check if we already have accounts
        existing_count = db.query(Account).count()
        if existing_count > 0:
            print(f"Found {existing_count} existing accounts.")
            response = input("Do you want to delete existing accounts and create new ones? (y/N): ")
            if response.lower() == 'y':
                db.query(Account).delete()
                db.commit()
                print("Deleted existing accounts.")
            else:
                print("Keeping existing accounts and adding new ones.")
        
        # Generate new accounts
        num_accounts = int(input("How many test accounts would you like to create? (default: 50): ") or "50")
        accounts = create_test_accounts(db, num_accounts)
        
        print(f"\nSuccessfully created {len(accounts)} test accounts!")
        print("\nSample of created accounts:")
        for account in accounts[:5]:  # Show first 5 accounts
            print(f"\nName: {account.name}")
            print(f"Industry: {account.industry}")
            print(f"Employees: {account.employee_count}")
            print(f"Revenue: ${account.annual_revenue:,}")
            print(f"Website: {account.website_url}")
            print("-" * 50)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 