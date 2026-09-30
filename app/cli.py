import typer
from tabulate import tabulate
from sqlmodel import select

from app.database import get_cli_session, create_db_and_tables, drop_all
from app.models import User, Game, Listing, Rental, Customer, DEPOSIT
from app.utilities.security import encrypt_password

cli = typer.Typer()


def get_customer(db, username: str) -> Customer:
    user = db.exec(select(User).where(User.username == username)).one_or_none()
    customer = db.get(Customer, user.id) if user else None
    if not customer:
        print(f"Customer '{username}' not found")
        raise typer.Exit(1)
    return customer


@cli.command()
def initialize():
    drop_all()
    create_db_and_tables()
    with get_cli_session() as db:
        for name in ["bob", "alice", "rick"]:
            user = User(username=name, email=f"{name}@mail.com",
                        password=encrypt_password(f"{name}pass"), role="customer")
            db.add(user)
            db.flush()
            customer = Customer(id=user.id)
            db.add(customer)
            db.add(customer.make_payment(DEPOSIT))
        for title in ["Elden Ring", "Mario Kart 8", "FC 26"]:
            db.add(Game(title=title))
        db.commit()
    print("Database initialized")


@cli.command()
def games():
    with get_cli_session() as db:
        rows = []
        for g in db.exec(select(Game)).all():
            for l in g.listings:
                rows.append({"game_id": g.id, "title": g.title, "listing_id": l.id,
                             "owner": l.owner.username, "price": l.price,
                             "available": l.is_available()})
            if not g.listings:
                rows.append({"game_id": g.id, "title": g.title})
        print(tabulate(rows, headers="keys"))


@cli.command()
def list_game(username: str, game_id: int, price: float, condition: str = "good"):
    with get_cli_session() as db:
        customer = get_customer(db, username)
        game = db.get(Game, game_id)
        if not game:
            return print(f"Game {game_id} not found")
        try:
            listing = customer.list_game(game, condition, price)
        except ValueError as e:
            return print(e)
        db.add(listing)
        db.commit()
        db.refresh(listing)
        print(f"Listing {listing.id}: '{game.title}' listed by {username} at {price:.2f}")


@cli.command()
def rent(username: str, listing_id: int):
    with get_cli_session() as db:
        customer = get_customer(db, username)
        listing = db.get(Listing, listing_id)
        if not listing:
            return print(f"Listing {listing_id} not found")
        try:
            rental = customer.rent_game(listing)
        except ValueError as e:
            return print(e)
        db.add(rental)
        db.commit()
        db.refresh(rental)
        print(f"Rental {rental.id}: {username} rented '{listing.game.title}', due {rental.due_date}")


@cli.command()
def return_game(username: str, rental_id: int, amount: float):
    with get_cli_session() as db:
        customer = get_customer(db, username)
        rental = db.get(Rental, rental_id)
        if not rental:
            return print(f"Rental {rental_id} not found")
        try:
            payment = customer.return_game(rental, amount)
        except ValueError as e:
            return print(e)
        db.add(payment)
        db.commit()
        print(f"Rental {rental_id} returned. Paid {amount:.2f}")


if __name__ == "__main__":
    cli()