"""PyDSA entry point: shows the intro and runs the main data structure menu."""

import utility
import my_array
import stack
import queue


def main():
    """Run the main data structure selection loop."""

    # Main selection loop; leaving a data structure returns control here
    while True:

        choice = input("""\n🏁 Which Linear Data Structure do you want to learn?
★1) Array
★2) Stack
★3) Queue

>>> """)

        match choice:

            # Array
            case "1":
                my_array.array_main()

            # Stack
            case "2":
                stack.stack_main()

            # Queue
            case "3":
                queue.queue_main()

            # Invalid
            case _:
                print("\n❌ Invalid code number!")


# Show the intro and start the program
utility.main_intro()
main()
