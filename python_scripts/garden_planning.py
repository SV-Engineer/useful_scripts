import numpy as np
import matplotlib as plt
import pandas as pd

from garden_beds import GardenBed

GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1zTqULrjwrdDliqccbx5MZBzw0mwPVeivbNfuxbTr-lE/export?format=csv&gid=1200757501"

def main():
  # Alpha   = GardenBed("alpha", 108.0, 34.0)
  # Bravo   = GardenBed("bravo", 89.5, 36.0)
  # Charlie = GardenBed("charlie", 92.5, 40.0)

  # Alpha.optimize_city_blocks()
  # Bravo.optimize_city_blocks()
  # Charlie.optimize_city_blocks()

  df = pd.read_csv(GOOGLE_SHEET_URL)
  pd.set_option('display.max_rows', df.shape[0]+1)

  print(df)



if __name__ == "__main__":
  main()
  