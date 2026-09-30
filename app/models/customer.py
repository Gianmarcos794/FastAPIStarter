from datetime import date

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from app.models.payment import Payment
from app.models.user import User
from app.models.listing import Listing
from app.models.rental import Rental
from app.models.game import Game

DEPOSIT = 20.0


class Customer(SQLModel, table=True):
    id: int = Field(foreign_key="user.id", primary_key=True)
    
    user: User = Relationship()
    payments: list["Payment"] = Relationship(back_populates="customer")
    listings: list["Listing"] = Relationship(back_populates="owner") 
    rentals: list["Rental"] = Relationship(back_populates="renter")
    
    
    @property
    def username(self) -> str:
        return self.user.username
    
    @property
    def password(self) -> str:
        return self.user.password
    
    def make_payment(self,amount: float, rental: Optional["Rental"] = None) -> "Payment":
        payment = Payment(amount=amount, customer_id=self.id, rental_id=rental.id if rental else None)
        return payment
    
    def list_game(self, game: "Game", condition: str, price: float) -> "Listing":
        listing = Listing(game_id=game.id, owner_id=self.id, condition=condition, price=price)
        return listing
    
    def rent_game(self, listing: "Listing") -> "Rental":
        rental = Rental(listing_id=listing.id, renter_id=self.id)
        return rental
    
    def return_game(self, rental: "Rental") -> None:
        rental.return_date = date.today()