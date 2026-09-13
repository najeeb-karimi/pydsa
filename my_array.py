"""Static, fixed-type array implementation.

The module is named my_array to avoid a conflict with Python's built-in array module.
"""

import utility


# ---------------------------------------------------------------------------
# Array class
# ---------------------------------------------------------------------------

class Array:
    """Fixed-size array that only accepts elements of a single data type."""

    def __init__(self, size, data_type, default_value=None):
        """Initialize the array with a size, data type and default value."""
        self.size = size
        self.data_type = data_type
        self.default_value = default_value
        self.array = [default_value] * size if default_value is None or isinstance(default_value, data_type) else [data_type()] * size

    def insert(self, index, value):
        """Insert an element at the given index."""
        if not isinstance(value, self.data_type):
            print(f"\n🚫 TypeError(Array can only contain elements of type {self.data_type.__name__}; item not inserted.)")
        else:
            if 0 <= index < self.size:
                self.array[index] = value
            else:
                print("\n🚫 IndexError(Array index out of bounds; item not inserted.)")

    def remove(self, index):
        """Remove the element at the given index by resetting it to the default value."""
        if 0 <= index < self.size:
            self.array[index] = self.default_value
        else:
            print("\n🚫 IndexError(Array index out of bounds. Deletion unsuccessful.)")

    def get(self, index):
        """Print the element at the given index."""
        if 0 <= index < self.size:
            print(f"\n👉 {self.array[index]}")
        else:
            print("\n🚫 IndexError(Array index out of bounds.)")

    def display(self):
        """Print the entire array."""
        print(f"\n👉 {self.array}")

    def size_check(self):
        """Print the size of the array."""
        size = self.size
        print(f"\n👉 Array size: {size}")

    def type_check(self):
        """Print the data type of the array."""
        data_type = self.data_type.__name__
        print(f"\n👉 Array Data Type: {data_type}")


# ---------------------------------------------------------------------------
# Array main function
# ---------------------------------------------------------------------------

def array_main():
    """Create an array and run the array operation menu."""
    array_intro("full")

    # Array type validation loop
    while True:
        array_type = input("\n🤔 Please specify the type of array. Write either str or int.\n>>> ")
        if array_type not in ("str", "int"):
            print("\n❌️ Either str or int!")
            continue
        break

    # Array size validation loop
    while True:
        try:
            array_size = int(input("\n↔️ Please specify the size of the array.\n>>> "))
        except ValueError:
            print("\n❌ Invalid, the size can only be an integer!️")
            continue
        else:
            break

    # Initialize the array
    if array_type == "str":
        array = Array(array_size, str)
    else:
        array = Array(array_size, int, 0)

    print(f"\n✅️ Here's your {array_type} array.", end="")
    array.display()

    # Operation selection loop
    while True:
        opr = input("""\n⚔️ Which operation do you want to perform with the ARRAY?
★0) Definition
★1) Insertion
★2) Deletion
★3) Indexing
★4) Size Check
★5) Type Check
★6) Displaying
★7) New Array
★8) New Data Structure
★9) Exit the Program

>>> """)

        if opr not in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            print("\n❌️ Invalid code number.")
            continue

        # Definition
        if opr == "0":
            array_intro("def")

        # Insertion
        elif opr == "1":

            choice = input("\n➕️ Type 1 for adding one item or anything else for filling up the entire array.\n>>> ")

            # Add a single item
            if choice == "1":
                item = input("\n✍️ Please write the item.\n>>> ")
                index = int(input("\n✍️ Please provide the index.\n>>> "))

                try:
                    if array_type == "int":
                        item = int(item)
                except ValueError:
                    pass

                array.insert(index, item)
                array.display()

            # Fill the entire array
            else:
                for i in range(array.size):
                    item = input(f"\n✍️ Please write the item for index {i}: ")
                    try:
                        if array_type == "int":
                            item = int(item)
                    except ValueError:
                        pass

                    array.insert(i, item)
                array.display()

        # Deletion
        elif opr == "2":
            index = int(input("\n✍️ Please provide the index of the item you want to remove.\n>>> "))
            array.remove(index)
            array.display()

        # Indexing
        elif opr == "3":
            index = int(input("\n✍️ Please provide the index of the item you want to get.\n>>> "))
            array.get(index)

        # Size check
        elif opr == "4":
            array.size_check()

        # Type check
        elif opr == "5":
            array.type_check()

        # Displaying
        elif opr == "6":
            array.display()

        # New array
        elif opr == "7":
            utility.clear()
            utility.main_intro()
            array_main()
            break

        # New data structure
        elif opr == "8":
            utility.clear()
            utility.main_intro()
            break

        # Exit the program
        elif opr == "9":
            exit()


# ---------------------------------------------------------------------------
# Array intro
# ---------------------------------------------------------------------------

def array_intro(condition):
    """Print the ASCII art and definition ("full") or only the definition ("def")."""
    array_ascii = """\n
   ____    .-------.    .-------.       ____       ____     __  
 .'  __ `. |  _ _   \   |  _ _   \    .'  __ `.    \   \   /  / 
/   '  \  \| ( ' )  |   | ( ' )  |   /   '  \  \    \  _. /  '  
|___|  /  ||(_ o _) /   |(_ o _) /   |___|  /  |     _( )_ .'   
   _.-`   || (_,_).' __ | (_,_).' __    _.-`   | ___(_ o _)'    
.'   _    ||  |\ \  |  ||  |\ \  |  |.'   _    ||   |(_,_)'     
|  _( )_  ||  | \ `'   /|  | \ `'   /|  _( )_  ||   `-'  /      
\ (_ o _) /|  |  \    / |  |  \    / \ (_ o _) / \      /       
 '.(_,_).' ''-'   `'-'  ''-'   `'-'   '.(_,_).'   `-..-'\n"""

    array_def = "\n🎯 An array is a fundamental linear data structure in computer science, consisting of a collection of elements, each identified by at least one array index or key. These elements are of the same data type and are stored in contiguous memory locations, allowing for efficient access and manipulation of data. Arrays are characterized by their fixed size, which is defined at the time of creation, and the ability to directly access any element in constant time using its index. This makes arrays particularly useful for implementing algorithms that require quick retrieval and update operations, as well as for storing data that can be easily sorted and searched."

    if condition == "full":
        print(array_ascii)
        print(array_def)
    elif condition == "def":
        print(array_def)


# Run the array module on its own
if __name__ == "__main__":
    array_main()
