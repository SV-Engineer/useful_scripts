import random

def main():
  family = [
    "Dak",
    #"Dan",
    #"Dav",
    "Mik",
    "Tan"#,
    #"Tay"
  ]

  selected = random.choice(family)
  print(f"Selected for gift is: {selected}")

if __name__ == "__main__":
  main()