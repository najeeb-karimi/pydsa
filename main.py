"""PyDSA entry point: shows the intro and runs the main data structure menu."""

import utility
import my_array
import stack
import queue
import linked_list
import tree
import graph


def main():
    """Run the main menu: pick a category, then a data structure within it."""

    # Category selection loop (linear vs non-linear). Choosing "New Data Structure"
    # inside any data structure breaks out of its menu and returns control here.
    while True:

        choice_1 = input("""\n📂 Which type of data structure do you want to learn?
★1) Linear data structures
★2) Non-linear data structures

>>> """)

        match choice_1:

            # Linear data structures
            case "1":
                while True:
                    choice_2 = input("""\n🏁 Which Linear Data Structure do you want to learn?
★1) Array
★2) Stack
★3) Queue
★4) Linked List

★0) Go Back

>>> """)
                    match choice_2:

                        # Array
                        case "1":
                            my_array.array_main()
                            break

                        # Stack
                        case "2":
                            stack.stack_main()
                            break

                        # Queue
                        case "3":
                            queue.queue_main()
                            break

                        # Linked List
                        case "4":
                            linked_list.linked_list_main()
                            break

                        # Go back
                        case "0":
                            main()
                            break

                        # Invalid
                        case _:
                            print("\n❌ Invalid code number!️")
                            continue

            # Non-linear data structures
            case "2":
                while True:
                    choice_2 = input("""\n Which Non-linear Data Structure do you want to learn?
★1) Tree
★2) Graph

★0) Go Back

>>> """)
                    match choice_2:

                        # Tree
                        case "1":
                            tree.tree_main()
                            break

                        # Graph
                        case "2":
                            graph.graph_main()
                            break

                        # Go back
                        case "0":
                            main()
                            break

                        # Invalid
                        case _:
                            print("\n❌ Invalid code number!️")
                            continue

            # Invalid
            case _:
                print("\n❌ Invalid code number!")


# Show the intro and start the program
utility.main_intro()
main()
