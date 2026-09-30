from sqlmodel import Field, SQLModel, Relationship
from datetime import date, datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.listing import Listing
    

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rental_id: Optional[int] = Field(default=None, foreign_key="rental.id")  
    customer_id: int = Field(foreign_key="customer.id")
    payment_date: date = Field(default_factory=date.today)
    amount: float

    customer: "Customer" = Relationship(back_populates="payments")
    rental: Optional["Rental"] = Relationship(back_populates="payments")
    
    def getAmount(self) -> float:
        return self.amount  
    
    def toJSON(self) -> dict:
        return {
            "id": self.id,
            "rental_id": self.rental_id,
            "customer_id": self.customer_id,
            "payment_date": self.payment_date.strftime("%Y-%m-%d"),
            "amount": self.amount,
        }