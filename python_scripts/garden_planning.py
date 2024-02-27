import numpy as np
import matplotlib as plt

from garden_beds import GardenBed


def main():
  Alpha   = GardenBed("alpha", 108.0, 34.0)
  Bravo   = GardenBed("bravo", 89.5, 36.0)
  Charlie = GardenBed("charlie", 92.5, 40.0)

  Alpha.optimize_city_blocks()
  Bravo.optimize_city_blocks()
  Charlie.optimize_city_blocks()


if __name__ == "__main__":
  main()
  