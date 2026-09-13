"""Hash table implementations with two collision resolution techniques.

Separate chaining (open hashing) and linear probing, from the open addressing (closed hashing) family.
"""

import utility


# ---------------------------------------------------------------------------
# Hash table with Separate Chaining (Open Hashing)
# ---------------------------------------------------------------------------

class ChainingHashTable:
    """Hash table where each bucket is a list, so colliding keys are chained in the same bucket."""

    def __init__(self, size):
        """Initialize the hash table with the given number of empty buckets."""
        self.size = size
        self.table = [[] for _ in range(size)]
        print(f"\n✅ Initialized hash table with {size} buckets.")
        print("ℹ️ Since Chaining uses another data structure for collision resolution, the hash table remains dynamic, so you need not worry about storage space!\n")

    def hash_function(self, key):
        """Return the bucket index for a key: its hash code modulo the table size."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Insert a key-value pair, or update the value if the key already exists; return a status message."""
        index = self.hash_function(key)
        # Update the value if the key is already in the bucket
        for kv in self.table[index]:
            if kv[0] == key:
                kv[1] = value
                return f"\n✅ Insertion successful. Updated key ({key}) with value ({value}) at index {index}."
        # Otherwise, append a new key-value pair to the bucket
        self.table[index].append([key, value])
        return f"\n✅ Insertion successful. Inserted key ({key}) with value ({value}) at index {index}."

    def lookup(self, key):
        """Look up a key and return a message with its index and value, or a not-found message."""
        index = self.hash_function(key)
        for kv in self.table[index]:
            if kv[0] == key:
                return f"\n✅ Searching successful. Key ({key}) found at index {index} with value ({kv[1]})."
        return f"\n❌ Searching successful. Key ({key}) not found."

    def delete(self, key):
        """Delete a key-value pair and return a status message."""
        index = self.hash_function(key)
        for i, kv in enumerate(self.table[index]):
            if kv[0] == key:
                del self.table[index][i]
                return f"\n✅ Deletion successful. Deleted key ({key}) from index {index}."
        return f"\n🚫 Deletion unsuccessful. Key ({key}) not found, nothing to delete."

    def display(self):
        """Print the hash table, one bucket per line."""
        # Bucket numbers are tracked separately; list.index() would repeat the same number for identical buckets
        total_buckets = len(self.table)
        indices = [index for index in range(total_buckets)]
        for bucket in self.table:
            print("🔹", indices.pop(0), bucket)


def chaining_main():
    """Create a separate chaining hash table and run its operation menu."""

    # Creation loop: build a hash table from scratch or load the preloaded example
    while True:
        example = input("""\n🛠️ Do you want to create a hash table yourself or use the preloaded example?
●1) Create a hash table
●2) Use the example
>>> """)
        match example:

            # Create a hash table
            case "1":
                # Table size validation loop; the size is the only input needed to create the table
                while True:
                    size = utility.input_verify("int", "the total number of buckets you want; in other words, the size of the hash table")
                    if size is not None and size >= 1:
                        chaining_ht = ChainingHashTable(size)
                        chaining_ht.display()
                        break
                    else:
                        print("\n🚫 Invalid data type. Hash table size must be an INT of at least 1.")
                        continue
                break

            # Use the example
            case "2":
                chaining_ht = ChainingHashTable(5)
                # The table can't be filled in directly: Python's hash() for strings changes between runs,
                # so the keys land in different buckets each time and hard-coded positions would be wrong
                chaining_ht.insert("Messi", "10")
                chaining_ht.insert("Apple", 1976)
                chaining_ht.insert(2024, -273.15)
                chaining_ht.insert("UFO", "Roswell, NM")
                # Display the example hash table
                print("👇🏻 Here's an example Chaining Hash Table:")
                chaining_ht.display()
                break

            # Invalid
            case _:
                print("\n❌ Invalid code number!")
                continue

    # Operation selection loop
    while True:
        opr = input("""\n⚔️ Which operation do you want to perform with the Chaining Hash Table?
★0) Definition
★1) Insertion
★2) Deletion
★3) Searching
★4) Displaying
★5) New Hash Table
★6) New Data Structure
★7) Exiting the Program

>>> """)
        match opr:

            # Definition
            case "0":
                hash_table_intro("def")

            # Insertion
            case "1":
                key = get_key()
                value = get_value()
                result = chaining_ht.insert(key, value)
                print(result)

            # Deletion
            case "2":
                key = get_key(text="key that you want to delete")
                result = chaining_ht.delete(key)
                print(result)

            # Searching
            case "3":
                key = get_key(text="key that you want to search for")
                result = chaining_ht.lookup(key)
                print(result)

            # Displaying
            case "4":
                print("\n👇🏻 Here's a display of your Hash Table:")
                chaining_ht.display()

            # New hash table
            case "5":
                utility.clear()
                hash_table_main()
                break

            # New data structure
            case "6":
                utility.clear()
                utility.main_intro()
                break

            # Exit the program
            case "7":
                exit()

            # Invalid
            case _:
                print("\n🚫 Invalid operation code!")


# ---------------------------------------------------------------------------
# Hash table with Linear Probing (Open Addressing / Closed Hashing)
# ---------------------------------------------------------------------------

class LinearProbingHashTable:
    """Hash table with one pair per slot; a collision moves on to the next free slot (linear probing)."""

    def __init__(self, size):
        """Initialize the hash table with the given number of empty slots."""
        self.size = size
        self.table = [None] * size
        print(f"\n✅ Initialized hash table with {size} slots.")

    def hash_function(self, key):
        """Return the home slot index for a key: its hash code modulo the table size."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Insert a key-value pair, or update the value if the key already exists; return a status message."""
        index = self.hash_function(key)
        original_index = index
        # Probe forward until an empty slot or the same key is found
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return f"\n✅ Insertion successful. Updated key ({key}) with value ({value}) at index {index}."
            index = (index + 1) % self.size
            # Coming back around to the starting slot means every slot is taken
            if index == original_index:
                return "\n🚫 Insertion unsuccessful. Hash table is full; cannot insert new key."
        self.table[index] = (key, value)
        return f"\n✅ Insertion successful. Inserted key ({key}) with value ({value}) at index {index}."

    def lookup(self, key):
        """Look up a key and return a message with its index and value, or a not-found message."""
        index = self.hash_function(key)
        original_index = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return f"\n✅ Searching successful. Key ({key}) found at index {index} with value ({self.table[index][1]})."
            index = (index + 1) % self.size
            if index == original_index:
                break
        return f"\n❌ Searching successful. Key ({key}) not found."

    def delete(self, key):
        """Delete a key-value pair, rehash the rest of its cluster and return a status message."""
        index = self.hash_function(key)
        original_index = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = None
                # Take out every pair that follows in the same cluster and insert it again,
                # so later lookups don't stop at the gap left by the deleted pair
                cluster = []
                next_index = (index + 1) % self.size
                while self.table[next_index] is not None:
                    cluster.append(self.table[next_index])
                    self.table[next_index] = None
                    next_index = (next_index + 1) % self.size
                for rehash_key, rehash_value in cluster:
                    self.insert(rehash_key, rehash_value)
                message = f"\n✅ Deletion successful. Deleted key ({key}) from index {index}."
                if cluster:
                    message += f"\n♻️ Rehashed {len(cluster)} key(s) from the same cluster."
                return message
            index = (index + 1) % self.size
            if index == original_index:
                break
        return f"\n🚫 Deletion unsuccessful. Key ({key}) not found, nothing to delete."

    def display(self):
        """Print the hash table, one slot per line."""
        # Slot numbers are tracked separately; list.index() would repeat the same number for identical slots
        total_slots = len(self.table)
        indices = [index for index in range(total_slots)]
        for slot in self.table:
            print("🔹", indices.pop(0), slot)


def linear_probing_main():
    """Create a linear probing hash table and run its operation menu."""

    # Creation loop: build a hash table from scratch or load the preloaded example
    while True:
        example = input("""\n🛠️ Do you want to create a hash table yourself or use the preloaded example?
●1) Create a hash table
●2) Use the example
>>> """)
        match example:

            # Create a hash table
            case "1":
                # Table size validation loop; the size is the only input needed to create the table
                while True:
                    size = utility.input_verify("int", "the total number of slots you want; in other words, the size of the hash table")
                    if size is not None and size >= 1:
                        linear_probing_ht = LinearProbingHashTable(size)
                        linear_probing_ht.display()
                        break
                    else:
                        print("\n🚫 Invalid data type. Hash table size must be an INT of at least 1.")
                        continue
                break

            # Use the example
            case "2":
                linear_probing_ht = LinearProbingHashTable(5)
                # The table can't be filled in directly: Python's hash() for strings changes between runs,
                # so the keys land in different slots each time and hard-coded positions would be wrong
                linear_probing_ht.insert("Messi", "10")
                linear_probing_ht.insert("Apple", 1976)
                linear_probing_ht.insert(2024, -273.15)
                print("👇🏻 Here's an example Linear Probing Hash Table:")
                linear_probing_ht.display()
                break

            # Invalid
            case _:
                print("\n❌ Invalid code number!")
                continue

    # Operation selection loop
    while True:
        opr = input("""\n⚔️ Which operation do you want to perform with the Linear Probing Hash Table?
★0) Definition
★1) Insertion
★2) Deletion
★3) Searching
★4) Displaying
★5) New Hash Table
★6) New Data Structure
★7) Exiting the Program

>>> """)
        match opr:

            # Definition
            case "0":
                hash_table_intro("def")

            # Insertion
            case "1":
                key = get_key()
                value = get_value()
                result = linear_probing_ht.insert(key, value)
                print(result)

            # Deletion
            case "2":
                key = get_key(text="key that you want to delete")
                result = linear_probing_ht.delete(key)
                print(result)

            # Searching
            case "3":
                key = get_key(text="key that you want to search for")
                result = linear_probing_ht.lookup(key)
                print(result)

            # Displaying
            case "4":
                print("\n👇🏻 Here's a display of your Hash Table:")
                linear_probing_ht.display()

            # New hash table
            case "5":
                utility.clear()
                hash_table_main()
                break

            # New data structure
            case "6":
                utility.clear()
                utility.main_intro()
                break

            # Exit the program
            case "7":
                exit()

            # Invalid
            case _:
                print("\n🚫 Invalid operation code!")


# ---------------------------------------------------------------------------
# Hash table main and intro functions
# ---------------------------------------------------------------------------

def hash_table_main():
    """Show the hash table intro and let the user pick a collision resolution technique.

    Once the chosen table's menu returns, control goes back to the main menu in main.py.
    """
    hash_table_intro("full")

    # Collision resolution type selection loop
    while True:
        hash_table_type = input("""\n🧪 Which type of collision resolution do you want in the hash table?
★1) Separate Chaining (Open Hashing)
★2) Linear Probing (from the Open Addressing [Closed Hashing] category)
>>> """)

        match hash_table_type:
            # Chaining
            case "1":
                chaining_main()
                break

            # Linear probing
            case "2":
                linear_probing_main()
                break

            # Invalid
            case _:
                print("\n🚫 Invalid collision resolution type code!")


def hash_table_intro(condition):
    """Print the ASCII art and definition ("full") or only the definition ("def")."""
    hash_table_ascii = r"""

.---.  .---.    ____       .-'''-. .---.  .---.         ,---------.    ____     _______     .---.       .-''-.   
|   |  |_ _|  .'  __ `.   / _     \|   |  |_ _|         \          \ .'  __ `. \  ____  \   | ,_|     .'_ _   \  
|   |  ( ' ) /   '  \  \ (`' )/`--'|   |  ( ' )          `--.  ,---'/   '  \  \| |    \ | ,-./  )    / ( ` )   ' 
|   '-(_{;}_)|___|  /  |(_ o _).   |   '-(_{;}_)            |   \   |___|  /  || |____/ / \  '_ '`) . (_ o _)  | 
|      (_,_)    _.-`   | (_,_). '. |      (_,_)             :_ _:      _.-`   ||   _ _ '.  > (_)  ) |  (_,_)___| 
| _ _--.   | .'   _    |.---.  \  :| _ _--.   |             (_I_)   .'   _    ||  ( ' )  \(  .  .-' '  \   .---. 
|( ' ) |   | |  _( )_  |\    `-'  ||( ' ) |   |            (_(=)_)  |  _( )_  || (_{;}_) | `-'`-'|___\  `-'    / 
(_{;}_)|   | \ (_ o _) / \       / (_{;}_)|   |             (_I_)   \ (_ o _) /|  (_,_)  /  |        \       /  
'(_,_) '---'  '.(_,_).'   `-...-'  '(_,_) '---'             '---'    '.(_,_).' /_______.'   `--------` `'-..-'
"""

    hash_table_def = """\n🎯 A hash table is a non-linear data structure that stores key-value pairs and uses a hash function to turn each key into an index of an underlying array, whose positions are called buckets or slots. Because the index is computed directly from the key, inserting, searching and deleting take O(1) time on average, which makes hash tables ideal for dictionaries, caches, database indexes and symbol tables. When two different keys hash to the same index, a collision occurs, so every hash table needs a collision resolution technique. The two main families are Open Hashing (Separate Chaining) and Closed Hashing (Open Addressing).

🌟 Separate Chaining stores every entry that hashes to the same index in a secondary structure attached to that bucket, usually a list. Colliding keys are simply added to the bucket's chain, so the table never fills up and can hold more entries than it has buckets. Inserting, searching and deleting take O(1) time on average, but degrade to O(n) in the worst case when many keys land in the same bucket. The trade-off is the extra memory used by the chains.

🌟 Linear Probing is an Open Addressing technique in which every entry is stored directly in one of the table's slots. When a key's home slot is taken, the table checks the next slot, then the next, wrapping around to the start, until it finds an empty one, and lookups follow the same path until they find the key or reach an empty slot. Linear probing is cache-friendly and needs no extra memory, but the table can hold at most as many entries as it has slots, and occupied slots tend to form clusters that make probing slower. Deleting also needs care, since emptying a slot would break the probe path of the keys after it, which is why this program rehashes the rest of the cluster after every deletion."""

    if condition == "full":
        print(hash_table_ascii)
        print(hash_table_def)
    elif condition == "def":
        print(hash_table_def)


# ---------------------------------------------------------------------------
# Input helpers for keys and values
# ---------------------------------------------------------------------------

def get_key(text="key"):
    """Ask for a key of any type until a valid one is entered; text customizes the prompt."""
    print("\n🔑 Specify the Key:")
    while True:
        key = utility.input_verify(msg=text)
        if key is None:
            print("\n🚫 Invalid data type for the key.")
            continue
        else:
            return key


def get_value(text="value"):
    """Ask for a value of any type until a valid one is entered; text customizes the prompt."""
    print("\n🚪 Specify the Value:")
    while True:
        value = utility.input_verify(msg=text)
        if value is None:
            print("\n🚫 Invalid data type for the value.")
            continue
        else:
            return value


# Run the hash table module on its own
if __name__ == "__main__":
    hash_table_main()
