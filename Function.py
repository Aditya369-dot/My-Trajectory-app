
FILEPATH = "todos.txt"

def get_todos(filepath=FILEPATH):
    """read a txt file using the read method and see the prior data in that file"""
    with open(filepath, 'r') as file:
        todos = file.readlines()
    return todos


def write_todos(todos_arg,filepath=FILEPATH):
    """Using the write method to store the new todos in that txt file"""
    with open(filepath, 'w') as file:
        file.writelines(todos_arg)


if __name__ == "__main__":
    print("Hello")
    print(get_todos())