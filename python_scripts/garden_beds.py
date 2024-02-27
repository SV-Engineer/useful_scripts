NUM_INFO_NL_WS = 7*" "
L_IDX          = 0
W_IDX          = 1

TRUE           = True
FALSE          = False

class GardenBed:
  def __init__(self, name, length, width) -> None:
    self.Name            = name
    self.L               = length
    self.W               = width
    self.Discarded       = []
    self.Block           = None
    self.AltBlock        = None

  def _info(self, info : str) -> None:
    print(f"INFO: {info}\n")

  def show_bed_info(self) -> None:
    print("#################################################################################")
    self._info(f"Garden bed {self.Name}:\n{NUM_INFO_NL_WS}* Length - {self.L} inches\n{NUM_INFO_NL_WS}* Width - {self.W} inches")

  def _calculate_num_squares(self, sq_dimensions : tuple) -> int:
    m           = self.L / sq_dimensions[L_IDX]
    n           = self.W / sq_dimensions[W_IDX]
    num_squares = 0
    temp        = 0
    if (n < m):
      temp = m
      m    = n
      n    = temp
    
    num_squares = ((m * (m + 1) * (2 * m + 1) / 6 + (n - m) * m * (m + 1) / 2))

    return int(num_squares)

  def _calculate_partial_square(self, sq_dimensions : tuple) -> int:
    m           = self.L / sq_dimensions[L_IDX]
    n           = self.W / sq_dimensions[W_IDX]
    num_squares = 0
    temp        = 0
    if (n < m):
      temp = m
      m    = n
      n    = temp
    
    num_squares = ((m * (m + 1) * (2 * m + 1) / 6 + (n - m) * m * (m + 1) / 2)) % 1

    return num_squares

  def _generate_block_sizes(self)->dict:
    sq_info = []
    for i in range(8, int(self.L + (1.0 - self.L % 1))):
      dimensions = (i, int(self.W / 2))
      size_info = {
        'N' : self._calculate_num_squares(dimensions),
        'P' : self._calculate_partial_square(dimensions),
        'L' : dimensions[L_IDX],
        'W' : dimensions[W_IDX]
      }

      sq_info.append(size_info)

      # Gonna overwrite them anyways so delete here instead of waiting for garbage collector
      del dimensions
      del size_info

    return sq_info

  def _find_greatest_num_blocks(self, blocks : list)->dict:
    if blocks == []:
      return None
    
    else:
      greatest = None

      for i, block in enumerate(blocks):
        if (block['N'] % 2 == 0):
          if greatest is not None:
            if (block['N'] > greatest['N']):
              greatest = block

            else:
              self.Discarded.append(block)

          else:
            greatest = block

        else:
          continue

    return greatest

  # pass output of _generate_block_sizes to me
  def _optimize_space(self, blocks : list) -> dict:
    chosen = self._find_greatest_num_blocks(blocks)
    n_diff = 0.0
    if (chosen['P'] > 0.20):
      for d in self.Discarded:
        n_diff = (abs(d['N'] - chosen['N']) / chosen['N']) * 100.0
        if (n_diff < 17.5 and (d['P'] < 0.20)):
          self.AltBlock = chosen
          chosen        = d
          break

    return chosen

  def show_discarded_choices(self):
    if (self.Block is not None) and (self.Discarded != []):
      for d in self.Discarded:
        if ((d['N'] > 5) and (d['P'] <= 0.20)):
          self._info(f"Size {d['N']} discarded with {d['P']} of a square on the end {d['L']} x {d['W']}")

  def optimize_city_blocks(self) -> None:
    self.show_bed_info()
    self.Block = self._optimize_space(self._generate_block_sizes())
    self._info(f"{self.Name} is optimized for blocks: {self.Block['N']} at dimensions of {self.Block['L']} x {self.Block['W']} (inches) and Partial of {self.Block['P']}")

    if self.AltBlock is not None:
      self._info(f"{self.Name} has alternate (original) block size: {self.AltBlock['N']} at dimensions of {self.AltBlock['L']} x {self.AltBlock['W']} (inches) and Partial of {self.AltBlock['P']}")

def main():
  pass

if __name__ == "__main__":
  main()