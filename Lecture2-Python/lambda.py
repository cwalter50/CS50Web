people = [
    {"name": "Harry", "house": "Gryffindor"},
    {"name": "Cho", "house": "Ravenclaw"},
    {"name": "Draco", "house": "Slytherin"}
]

# need to tell sort, how to sort dictionaries

def f(person):
    return person["name"]

people.sort(key=f)

# or you can just do this...

people.sort(key=lambda person:person["name"])


print(people)