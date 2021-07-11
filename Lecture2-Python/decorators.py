def announce(f):
    def wrapper():
        print("About to run the function...")
        f()
        print("Done with function")
    return wrapper

# add announce decorator to a function with the @ symbol
@announce
def hello():
    print("Hello, World!")


hello()