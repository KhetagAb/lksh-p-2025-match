#!/usr/bin/env python3

import db

import itertools
import os
import random
import string
import sys


MATERIALS = ["stone", "marble", "gold", "wood", "concrete", "brick", "sandstone",
                "glass", "obsidian", "bedrock"]
CITIES = ["Novosibirsk", "Moscow", "St. Petersburg", "Gelendzhik", "Vladivostok",
            "Petrozavodsk", "Ekaterinburg", "Sevastopol", "Sochi", "Perm"]


def generate_random_db(seed=None):
    if seed is not None:
        random.seed(seed)
    
    n = lambda: random.randrange(1, 100)

    d = db.Database()

    d.cities = [db.City(name=city) for city in CITIES]
    d.materials = [db.Material(name=material) for material in MATERIALS]
    d.buyers = [db.Buyer(name=f"R2D{i}", surname=f"C{i}PO") for i in range(100)]
    d.owners = [db.Owner(name=f"X AE-{i}", surname="Musk") for i in range(100)]

    buyer_materials = {
        buyer: random.sample(d.materials[:-1], random.randrange(1, len(d.materials) // 2))
        for buyer in d.buyers
    }
    buyer_cities = {
        buyer: random.sample(d.cities[:-1], random.randrange(1, len(d.cities) // 2))
        for buyer in d.buyers
    }

    d.bids = [db.Bid(
        min_area=n(),
        max_price=n(),
        city=random.choice(buyer_cities[buyer]),
        buyer=buyer,
        materials=random.sample(
            buyer_materials[buyer],
            random.randrange(len(buyer_materials[buyer])),
        ),
    ) for buyer in (random.choice(d.buyers) for _ in range(500))]

    owner_materials = {
        owner: random.sample(d.materials[1:], random.randrange(1, len(d.materials)))
        for owner in d.owners
    }
    owner_cities = {
        owner: random.sample(d.cities, random.randrange(1, len(d.cities)))
        for owner in d.owners
    }

    d.buildings = [db.Building(
        name=f"Object {i}",
        area=n(),
        price=n(),
        city=random.choice(owner_cities[owner]),
        owner=owner,
        materials=random.sample(
            owner_materials[owner],
            random.randrange(len(owner_materials[owner])),
        ),
    ) for i, owner in enumerate(random.choice(d.owners[:-3]) for _ in range(500))]

    for objects in (d.cities, d.materials, d.buyers, d.owners, d.bids, d.buildings):
        random.shuffle(objects)

    return d


def index(n):
    def inner(func):
        func._index = n
        return staticmethod(func)
    return inner


class Tests:
    @index(1)
    def test_simple_select(d):
        return [
            (b.name, b.area, b.price, b.city.name) for b in d.buildings
            if b.area > 30 and b.price < 50
        ]
    
    @index(2)
    def test_gold_or_marble(d):
        return [
            (b.name,) for b in d.buildings
            if any(m.name in ("gold", "marble") for m in b.materials)
        ]

    @index(3)
    def test_no_gelendzhik(d):
        return [
            (b.name, b.surname)
            for b in set(d.buyers)
                - set(bid.buyer for bid in d.bids if bid.city.name == "Gelendzhik")
        ]
    
    @index(4)
    def test_unused_material(d):
        buyer_materials = {buyer: set(d.materials) for buyer in d.buyers}
        for bid in d.bids:
            buyer_materials[bid.buyer] -= set(bid.materials)
        return [
            (buyer.name, buyer.surname, material.name)
            for buyer in d.buyers
            for material in buyer_materials[buyer]
        ]

    @index(5)
    def test_area_above_avg(d):
        avg = lambda lst: sum(lst) / len(lst)
        avg_area = avg([b.area for b in d.buildings])
        city_avg_area = {
            city: avg([b.area for b in d.buildings if b.city == city])
            for city in d.cities
        }
        return [(c.name,) for c, a in city_avg_area.items() if a > avg_area]

    @index(6)
    def test_most_expensive_building(d):
        owner_max_price = {owner: None for owner in d.owners}
        for building in d.buildings:
            max_price = owner_max_price[building.owner]
            if max_price is None or max_price < building.price:
                owner_max_price[building.owner] = building.price
        return [
            (owner.name, owner.surname, max_price)
            for owner, max_price in owner_max_price.items()
        ]
    
    @index(7)
    def test_object_101(d):
        obj = next(b for b in d.buildings if b.name == "Object 101")
        return [
            (buyer.name, buyer.surname)
            for buyer in set(
                bid.buyer
                for bid in d.bids
                if obj.area >= bid.min_area
                    and obj.price <= bid.max_price
                    and obj.city == bid.city
                    and not set(bid.materials) - set(obj.materials)
            )
        ]
    
    @index(8)
    def test_sellable_count_by_city(d):
        result = {city: 0 for city in d.cities}
        for building in d.buildings:
            has_buyer = any(
                building.area >= bid.min_area
                    and building.price <= bid.max_price
                    and building.city == bid.city
                    and not set(bid.materials) - set(building.materials)
                for bid in d.bids
            )
            result[building.city] += int(has_buyer)
        return [(city.name, count) for city, count in result.items()]


def run_tests(index_to_query, test_index=None):
    tests = [getattr(Tests, attr) for attr in dir(Tests) if attr.startswith("test_")]

    for test in sorted(tests, key=lambda t: t._index):
        if test_index is not None and test_index != test._index:
            continue

        assert test._index in index_to_query, f"failed to find query #{test._index}"
        query = index_to_query[test._index]

        for _ in range(10):
            seed = random.randrange(2 ** 32)
            database = generate_random_db(seed)
            expected_answer = test(database)

            try:
                user_answer = database.execute_query(query)
                if set(expected_answer) != set(user_answer):
                    database.dump("debug.db")
                    dump_answers("debug.txt", expected_answer, user_answer)
                    raise AssertionError("wrong answer, see debug.txt and debug.db")
            except Exception:
                print(f"Test #{test._index} failed, seed: {seed}")
                print(f"Parsed query:\n{query}\n")
                raise
        
        print(f"Passed test #{test._index}")
    
    print("OK!")


def dump_answers(path, expected_answer, got_answer):
    with open(path, "w") as f:
        f.write(">>> EXPECTED ANSWER:\n")
        for tp in sorted(expected_answer):
            f.write(f"{tp}\n")
        f.write("\n>>> GOT ANSWER:\n")
        for tp in sorted(got_answer):
            f.write(f"{tp}\n")


def read_queries(path):
    with open(path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    index_to_query = {}
    
    for i in itertools.count(start=1):
        header = f"{i}.---"
        try:
            start_index = lines.index(header)
        except ValueError:
            break
        assert "---" in lines[start_index+1:], f"failed to find '---' footer for query #{i}"
        end_index = lines.index("---", start_index+1)
        index_to_query[i] = "\n".join(lines[start_index+1:end_index])
    
    return index_to_query


def main():
    queries_path = sys.argv[1]
    test_index = None
    if len(sys.argv) > 2:
        test_index = int(sys.argv[2])
    index_to_query = read_queries(queries_path)
    run_tests(index_to_query, test_index)


if __name__ == "__main__":
    main()
