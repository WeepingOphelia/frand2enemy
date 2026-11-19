
import fullrand
import name

def main_menu():
  while True:
    print(
      """
      Welcome to the Frand2Enemy Character Generator!
      
      We hope your day is going well.

      Select Option:
      1. Raw AF
      2. Select Temperature
      3. Fully Cooked - (NOT YET IMPLEMENTED)
      4. Random Name Generator
      5. Exit
      """
    )
    selection = input("<(^_^<) <(^_^)> (>^_^)> ? ")

    match selection:
      case "1":
        fullrand.rawAF(0)
      case "2":
        x = True
        while x:
          lvl = input("Enter desired character level (1-20) - ")
          try: 
            lvl = int(lvl)
          except Exception as e:
            print(f"Do you know what a number is? {e}")
            continue
          if 1 <= lvl <= 20:
            x = False
            fullrand.rawAF(lvl)
          else:
            print(f"Can you count or...?")
      case "3":
        print("Can you read???")
      case "4":
        print(name.randName())
      case "5":
        print("Exiting...")
        exit()
      case _:
        print("So you have chosen death...")

if __name__ == "__main__":
  main_menu()