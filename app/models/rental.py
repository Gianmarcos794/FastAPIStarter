from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import date

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.listing import Listing
    from app.models.payment import Payment
    
rental_days = 7
late_fee_per_day = 5.0

class Rental(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    listing_id: int = Field(foreign_key="listing.id")
    renter_id: int = Field(foreign_key="customer.id")
    rental_date: date = Field(default_factory=date.today)
    return_date: Optional[date] = None

    listing: "Listing" = Relationship(back_populates="rentals")
    renter: "Customer" = Relationship(back_populates="rentals")
    payments: list["Payment"] = Relationship(back_populates="rental")