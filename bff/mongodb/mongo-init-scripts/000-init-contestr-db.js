const students = [
    {parallel: "P", name: "Кузнецов Илья", sex: "male", tg_username: "dmkjfs"},
    {parallel: "P", name: "Григорьева Ирина", sex: "female", tg_username: "GrigorevaIA"},
    {parallel: "P", name: "Подыряка Евгений", sex: "male", tg_username: "icelayer"},
    {parallel: "P", name: "Щепарева Мария", sex: "female", tg_username: "masha_ee"},
    {parallel: "P", name: "Якушев Шоно", sex: "male", tg_username: "Shonoy"},
    {parallel: "P", name: "Шурыгин Егор", sex: "male", tg_username: "shurygin_egor"},
    {parallel: "P", name: "Одинцов Тимофей", sex: "male", tg_username: "timodi"},
    {parallel: "P", name: "Кокорев Вадим", sex: "male", tg_username: "VadimKokorev"},
    {parallel: "P", name: "Макаров Михаил", sex: "male", tg_username: "zog34bro"},
    {parallel: "admin", name: "Дзестелов Хетаг", sex: "male", tg_username: "abramkht"}
]
db = db.getSiblingDB("match");
db.students.insertMany(students);