# Create an empty set
s = set()

#add elements to set

s.add(1)
s.add(2)
s.add(3)
s.add(4)
s.add(3) # this will do nothing, because each item in the set needs to be unique and we already have a 3

s.remove(2) # this removes the number 2, not the value at index 2

print(s)

print(f"the set has {len(s)} elements")

