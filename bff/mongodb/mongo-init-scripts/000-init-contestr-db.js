db = db.getSiblingDB("match");
students = db.getCollection("students")
students.insertOne({
    "tg_username": "abramkht",
    "name": "Хетаг Дзестелов"
})