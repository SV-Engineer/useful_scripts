import random

def main():
  family = [
    "Dakota",
    "Dana",
    #"Darcy",
    #"David",
    "Mike",
    #"Maggie",
    "Tanis"#,
    #"Taylor"
  ]

  selected = random.choice(family)
  print(f"Selected for gift is: {selected}")

if __name__ == "__main__":
  main()