# src/daos/user_dao_mongo.py
"""
UserDAO MongoDB
Auteur : Ayman Zahir
"""
import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from models.user import User


class UserDAOMongo:
    def __init__(self):
        load_dotenv(find_dotenv())

        host = os.getenv("MONGODB_HOST", "mongo")
        db_name = os.getenv("MONGODB_DB_NAME") or os.getenv("MYSQL_DB_NAME") or "mydb"
        user = os.getenv("DB_USERNAME")
        pwd = os.getenv("DB_PASSWORD")

        if user and pwd:
            uri = f"mongodb://{user}:{pwd}@{host}:27017/?authSource=admin"
        else:
            uri = f"mongodb://{host}:27017"

        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.col = self.db["users"]

        self.col.create_index("id", unique=True)
        self._ensure_seed()


    def _ensure_seed(self):
        """Ajoute les 3 utilisateurs de base s'ils manquent (sans écraser l'existant)."""
        base = [
            {"id": 1, "name": "Ada Lovelace",   "email": "alovelace@example.com"},
            {"id": 2, "name": "Adele Goldberg", "email": "agoldberg@example.com"},
            {"id": 3, "name": "Alan Turing",    "email": "aturing@example.com"},
        ]
        for u in base:
            self.col.update_one({"id": u["id"]}, {"$setOnInsert": u}, upsert=True)

    def _next_id(self) -> int:
        last = self.col.find_one({}, {"_id": 0, "id": 1}, sort=[("id", -1)])
        return (last["id"] + 1) if last and "id" in last else 1


    def select_all(self):
        """Retourne List[User] triée par id croissant."""
        docs = self.col.find({}, {"_id": 0}).sort("id", 1)
        return [User(d.get("id"), d.get("name"), d.get("email")) for d in docs]

    def insert(self, user: User) -> int:
        """Insère un utilisateur et retourne son id (int)."""
        new_id = self._next_id()
        self.col.insert_one({"id": new_id, "name": user.name, "email": user.email})
        return new_id

    def update(self, user: User) -> bool:
        """
        Met à jour name/email d'un utilisateur par son id.
        Retourne True si un document correspondant existe (interchangeable avec MySQL).
        """
        res = self.col.update_one(
            {"id": user.id},
            {"$set": {"name": user.name, "email": user.email}},
        )
        return res.matched_count == 1

    def delete(self, user_id: int) -> bool:
        """Supprime un utilisateur par id. Retourne True si 1 document supprimé."""
        res = self.col.delete_one({"id": user_id})
        return res.deleted_count == 1


    def delete_all(self):
        """Vide la collection (utile pour certains tests)."""
        self.col.delete_many({})

    def close(self):
        try:
            self.client.close()
        except Exception:
            pass