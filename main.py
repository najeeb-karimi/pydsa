"""PyDSA entry point: shows the intro and runs the main data structure menu."""

import utility


def main():
    """Run the main data structure selection loop."""

    # Main selection loop; leaving a data structure returns control here
    while True:

        choice = input("""\n🏁 Which Linear Data Structure do you want to learn?
★1) Array

>>> """)

        match choice:

            # Array
            case "1":
                print("\n🚧 Array is coming soon!")

            # Invalid
            case _:
                print("\n❌ Invalid code number!")


# Show the intro and start the program
utility.main_intro()
main()
