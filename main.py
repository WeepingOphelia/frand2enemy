import fullcook
import fullrand
import levelselect

def main_menu():
  while True:
    print(
      """
      Welcome to the Frand2Enemy Character Generator!
      
      We hope your day is going well.

      Select Option:
      1. Raw AF
      2. Select Temperature
      3. Fully Cooked
      4. Exit
      """
    )
    selection = input("<(^_^<) <(^_^)> (>^_^)> ? ")

    match selection:
      case "1":
        fullrand.rawAF()
      case "2":
        levelselect.lvlSelect()
      case "3":
        fullcook.wellDone()
      case "4":
        print("Exiting...")
        exit()
      case _:
        print("So you have chosen death...")

if __name__ == "__main__":
  main_menu()