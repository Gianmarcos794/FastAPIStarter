from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.listing import Listing


class Game(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)

    listings: list["Listing"] = Relationship(back_populates="game")

    def toJSON(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
        }