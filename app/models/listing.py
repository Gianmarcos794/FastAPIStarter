from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, Optional
from enum import Enum
from typing import Optional
from datetime import datetime

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.rental import Rental
    from app.models.game import Game
    
class ListingStatus(str, Enum):
    AVAILABLE = "available"
    RENTED = "rented"
    PENDING = "pending"
    

class Listing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    owner_id: int = Field(foreign_key="customer.id")
    condition: str
    availability: ListingStatus = Field(default=ListingStatus.AVAILABLE)
    price: float
    date_listed: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    game: "Game" = Relationship(back_populates="listings")
    owner: "Customer" = Relationship(back_populates="listings")
    rentals: list["Rental"] = Relationship(back_populates="listing")
    
    def set_availability(self, status: ListingStatus):
        self.availability = status
    
    def is_available(self) -> bool:
        return self.availability == ListingStatus.AVAILABLE
    
    def toJSON(self) -> dict:
        return {
            "id": self.id,
            "game_id": self.game_id,
            "owner_id": self.owner_id,
            "condition": self.condition,
            "availability": self.availability.value,
            "price": self.price,
            "date_listed": self.date_listed,
        }