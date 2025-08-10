from dataclasses import dataclass, field
from typing import List
import sqlite3
import os


@dataclass(eq=False)
class City:
    name: str


@dataclass(eq=False)
class Material:
    name: str


@dataclass(eq=False)
class Buyer:
    name: str
    surname: str


@dataclass(eq=False)
class Owner:
    name: str
    surname: str


@dataclass(eq=False)
class Bid:
    min_area: int
    max_price: int
    city: City
    buyer: Buyer
    materials: List[Material] = field(default_factory=list)


@dataclass(eq=False)
class Building:
    name: str
    area: int
    price: int
    city: City
    owner: Owner
    materials: List[Material] = field(default_factory=list)


@dataclass
class Database:
    cities: List[City] = field(default_factory=list)
    materials: List[Material] = field(default_factory=list)
    buyers: List[Buyer] = field(default_factory=list)
    owners: List[Owner] = field(default_factory=list)
    bids: List[Bid] = field(default_factory=list)
    buildings: List[Building] = field(default_factory=list)

    def execute_query(self, query):
        conn = self._populate_db(":memory:")
        return conn.execute(query).fetchall()
    
    def dump(self, path):
        if os.path.exists(path):
            os.unlink(path)
        self._populate_db(path)
    
    def _populate_db(self, path):
        conn = sqlite3.connect(path)
        self._create_tables(conn)
        self._insert_rows(conn)
        return conn
    
    @staticmethod
    def _create_tables(conn):
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r") as f:
            script = f.read()
        conn.executescript(script)
    
    def _insert_rows(self, conn):
        object_to_id = {}
        for objects in (
            self.cities,
            self.materials,
            self.buyers,
            self.owners,
            self.bids,
            self.buildings,
        ):
            for id_, obj in enumerate(objects):
                object_to_id[id(obj)] = id_

        for objects in (
            self.cities,
            self.materials,
            self.buyers,
            self.owners,
            self.bids,
            self.buildings,
        ):
            for obj in objects:
                table = obj.__class__.__name__.lower()
                column_values = tuple(self._extract_column_values(obj, object_to_id).items())
                conn.execute(
                    "INSERT INTO {table}({columns}) VALUES ({values})".format(
                        table=table,
                        columns=",".join(column for column, _ in column_values),
                        values=",".join("?" * len(column_values)),
                    ),
                    tuple(value for _, value in column_values)
                )
        
        for objects in (self.buildings, self.bids):
            for id_, (obj, mat) in enumerate((obj, mat) for obj in objects for mat in obj.materials):
                conn.execute(
                    "INSERT INTO {0}_material(id, {0}_id, material_id) VALUES (?, ?, ?)".format(
                        obj.__class__.__name__.lower(),
                    ),
                    (id_, object_to_id[id(obj)], object_to_id[id(mat)]),
                )

        conn.commit()
    
    @staticmethod
    def _extract_column_values(obj, object_to_id):
        result = {"id": object_to_id[id(obj)]}
        for field in obj.__dataclass_fields__:
            value = getattr(obj, field)
            if isinstance(value, (int, str)):
                result[field] = value
            elif not isinstance(value, list):
                result[f"{field}_id"] = object_to_id[id(value)]
        return result
