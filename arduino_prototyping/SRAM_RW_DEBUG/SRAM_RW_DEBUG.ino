/** @file SRAM_RW_DEBUG
 * @author Austin - svengineer 
 * @brief Adhoc code to emulate expeted behavior for an SRAM controller.
 *
 * @par Description
 * This code exists to utilize an Arduino Nano to emulate the signal pattern a
 * 6116SA25TPG SRAM (2kB) expects for reads and writes. This code is intended to
 * provide a sanity check before building control hardware. To reduce the amount
 * of bread-boarding required, nibbles are being utilized rather than bytes.
 * Address bits [10:4] are tied low and bits [3:0] are used. I/O bits [7:4] are
 * left floating and bits [3:0] are used.
 *
 * @note RMW - read-modify-write
 *
 */

/** @brief EXISTS for personal preference. */
#define TRUE                        true
/** @brief EXISTS for personal preference in conveying negative logic. */
#define nTRUE                       (!TRUE)
/** @brief EXISTS for personal preference. */
#define FALSE                       false
/** @brief EXISTS for personal preference in conveying negative logic. */
#define nFALSE                      (!FALSE)


/** @brief The Arduino Nano port B (bits[5:0]) is used for emulating control logic. */
#define SRAM_CTRL_PORT              PORTB


/** @brief The Arduino Nano port D (bits[7:0]) is used for reading and writing data. */
#define SRAM_DATA_PORT              PORTD
/** @brief The address to read the port data from. */
#define SRAM_READ_PORT              PIND


/** @brief Pass this to the macros @ref SRAM_CTRL_PORT_EN and @ref SRAM_DATA_PORT_EN. */
#define ENABLE_PORT                 TRUE
/** @brief Pass this to the macros @ref SRAM_CTRL_PORT_EN and @ref SRAM_DATA_PORT_EN. */
#define DISABLE_PORT                FALSE


/** @brief Writing data to the SRAM */
#define ENABLE_DATA_IN              TRUE
/** @brief Reading data from the SRAM */
#define ENABLE_DATA_OUT             nTRUE


// CONTROL PORT MACROS
/** @brief The low 6 bits are used; bits 7 and 6 are reserved. */
#define SRAM_CTRL_PORT_EN(X)        DDRB = X ? (DDRB | (uint8_t) 0x3F) : (DDRB & ((uint8_t) (~0x3F)))


/** @brief This code is only utilizing 4 address lines; PORTB[3:0] are assigned and PORTB[5:4] are utilized else where. Thus, RMWs.*/
#define ADDRESS_MASK(A)             ((((uint8_t) A) & ((uint8_t) 0x0FU)) << 0)
/** @brief Implements a RMW to clear the assigned port address bits and logical OR in the desired address.
 * @note This implementation is lazy and inefficient, use a variable instead of 2 RMWs.
 */
#define SRAM_SET_ADDRESS(A)         SRAM_CTRL_PORT &= ((uint8_t) 0xF0U); \
                                    SRAM_CTRL_PORT |= (ADDRESS_MASK(A))


/** @brief The bit in PORTB assigned to control the SRAM /CS. */
#define SRAM_CHIP_SELECT_BIT        ((uint8_t) 0x1U << 5)
/** @brief The SRAM CS is active low, so this macro inverts the logic to set it to appropriate logic TRUE or logic FALSE; i.e. just pass true or false to enable and disable the SRAM input respectively. */
#define SRAM_CS(X)                  SRAM_CTRL_PORT = (X) ? (SRAM_CTRL_PORT & ~SRAM_CHIP_SELECT_BIT)  : (SRAM_CTRL_PORT | SRAM_CHIP_SELECT_BIT)


/** @brief The bit in PORTB assigned to control the SRAM /WE. */
#define SRAM_WRITE_ENABLE_BIT       ((uint8_t) 0x1U << 4)
/** @brief The SRAM WE is active low, so this macro inverts the logic to set it to appropriate logic TRUE or logic FALSE; i.e. just pass true or false to enable and disable the SRAM input respectively. */
#define SRAM_WE(X)                  SRAM_CTRL_PORT = (X) ? (SRAM_CTRL_PORT & ~SRAM_WRITE_ENABLE_BIT) : (SRAM_CTRL_PORT | SRAM_WRITE_ENABLE_BIT)


// DATA PORT MACROS
/** @brief Modifies PORTD to change between input and output.
 * @note The @ref ENABLE_DATA_IN means the port is an output because the SRAM is taking data in.
 * @note The @ref ENABLE_DATA_OUT means the port is an input because the SRAM is outputting data.
 */
#define SRAM_DATA_PORT_EN(X)        DDRD            = X ? (DDRD | (uint8_t) 0xF0)            : (DDRD & ((uint8_t) (0x0F)))

/** @brief When in input mode, the pull up resistors should be enabled? */
#define SRAM_DATA_PORT_EN_PU                        ((uint8_t) 0xFF)
/** @brief When in input mode, the pull up resistors should be disabled? */
#define SRAM_DATA_PORT_DIS_PU                       ((uint8_t) 0x00)

/** @brief Data to write to the SRAM. */
#define SRAM_DATA(X)                SRAM_DATA_PORT  &= ((uint8_t) 0x0F);     \
                                    SRAM_DATA_PORT  |= (((uint8_t) X) << 4)


// Function forward declarations
void read_sram_address(uint8_t, uint8_t*);
void write_sram_address(uint8_t, uint8_t);
void unit_test_0001(void);
void unit_test_0002(void);
void unit_test_0003(void);

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);

  // SET UP SRAM CONTROL TO BE FULLY DISABLED ON START UP.
  SRAM_CS(false);
  SRAM_WE(false);
  SRAM_CTRL_PORT_EN(ENABLE_PORT);

  // SETUP THE DATA PORT
  // WRITE all ones to the port data so that the pull up resistors will be enabled when the DATA port is set to input.
  SRAM_DATA(SRAM_DATA_PORT_DIS_PU);
  // Set up the data port as input.
  SRAM_DATA_PORT_EN(ENABLE_DATA_OUT);
  
}

void loop()
{
  unit_test_0001();
  unit_test_0002();
  unit_test_0003();
}

/** @fn void read_sram_address(uint8_t address, uint8_t* data)
 * @brief Reads data from the provided address in the SRAM.
 *
 * @par Description
 * This function implements data sheet Timing Waveform of Read Cycle No. 3.
 * Furthermore, input /WE must equal nFALSE for Read Cycle. The address must
 * be valid prior (or coincident) to /CS == nTRUE. Input /OE is tied to the
 * GND rail.
 *
 * @param address
 * Desired read location.
 *
 * @param data
 * Read data from the address (pass variable by reference).
 *
 */
void read_sram_address(uint8_t address, uint8_t* data)
{

  // 1. Set the data port to be input with pull up resistors disabled.
  SRAM_DATA(SRAM_DATA_PORT_DIS_PU);
  SRAM_DATA_PORT_EN(ENABLE_DATA_OUT);

  // 2. Set address and use chip select to trigger a read.
  SRAM_SET_ADDRESS(address);
  delayMicroseconds(1);
  SRAM_CS(TRUE);

  // 3. Short delay (1us is over-kill but the timing will not be tight for this use case; SRAM is ready on order of nano-seconds).
  delayMicroseconds(1);

  // 4. Grab data.
  *data = ((((uint8_t) SRAM_READ_PORT) >> 4) & ((uint8_t) 0xF));

  // 5. Turn off chip select.
  SRAM_CS(FALSE);
  
} /* read_sram_address */

/** @fn void write_sram_address(uint8_t address, uint8_t data)
 * @brief Writes data to the provided address in the SRAM.
 *
 * @param address
 * Desired write location.
 *
 * @note Either CS or WE must be high during an address transition.
 *
 * @param data
 * Desired data to write
 *
 */
void write_sram_address(uint8_t address, uint8_t data)
{
  char buffer[100];
  // /CS controlled write cycle.
  // 1. /WE == nTRUE - THE MACRO INVERTS THE LOGIC
  // 2. ADDRESS and Data setup; possibly short delay?
  // 3. /CS == nTRUE - THE MACRO INVERTS THE LOGIC
  // 4. Wait for write to finish.
  // 5. /CS == nFALSE - THE MACRO INVERTS THE LOGIC
  // 6. /WE == nFALSE - THE MACRO INVERTS THE LOGIC
  // 7. Repeat as needed.

  // Step 1
  #ifdef DEBUG
    memset(buffer, 0, sizeof(buffer));
    sprintf(buffer, "INFO - WRITE SRAM - Set WE to nTRUE; currently: (%0d)\n\0", (bool) (PINB & SRAM_WRITE_ENABLE_BIT));
    Serial.print(buffer);
  #endif

  SRAM_WE(TRUE);

  #ifdef DEBUG
    memset(buffer, 0, sizeof(buffer));
    sprintf(buffer, "INFO - WRITE SRAM - WE is now: (%0d)\n\0", (bool) (PINB & SRAM_WRITE_ENABLE_BIT));
    Serial.print(buffer);
  #endif

  // Step 2
  SRAM_DATA_PORT_EN(ENABLE_DATA_IN);
  SRAM_SET_ADDRESS(address);

  #ifdef DEBUG
    memset(buffer, 0, sizeof(buffer));
    sprintf(buffer, "INFO - WRITE SRAM - Set ADRESS to  (0x%02x)\n\0", (bool) (PINB & ((uint8_t) 0x0F)));
    Serial.print(buffer);
  #endif

  SRAM_DATA(data);
  delayMicroseconds(1);

  // Step 3
  #ifdef DEBUG
    memset(buffer, 0, sizeof(buffer));
    sprintf(buffer, "INFO - WRITE SRAM - Set CS to nTRUE; currently: (%0d)\n\0", (bool) (PINB & SRAM_CHIP_SELECT_BIT));
    Serial.print(buffer);
  #endif

  SRAM_CS(TRUE);

  #ifdef DEBUG
    memset(buffer, 0, sizeof(buffer));
    sprintf(buffer, "INFO - WRITE SRAM - CS is now: (%0d)\n\0", (bool) (PINB & SRAM_CHIP_SELECT_BIT));
    Serial.print(buffer);
  #endif

  delayMicroseconds(2);

  // Step 5
  #ifdef DEBUG
    memset(buffer, 0, sizeof(buffer));
    sprintf(buffer, "INFO - WRITE SRAM - Set WE to nFALSE; currently: (%0d)\n\0", (bool) (PINB & SRAM_WRITE_ENABLE_BIT));
    Serial.print(buffer);
  #endif

  SRAM_CS(FALSE);

  #ifdef DEBUG
    memset(buffer, 0, sizeof(buffer));
    sprintf(buffer, "INFO - WRITE SRAM - WE is now: (%0d)\n\0", (bool) (PINB & SRAM_WRITE_ENABLE_BIT));
    Serial.print(buffer);
  #endif

  // Step 6
  SRAM_DATA_PORT_EN(ENABLE_DATA_OUT);
  SRAM_DATA(SRAM_DATA_PORT_DIS_PU);
  SRAM_WE(FALSE);

} /* write_sram_address */

/** @fn void unit_test_0001(void)
 * @brief Reads contents of SRAM on power on and prints it out.
 *
 * @par Description
 * Reads contents of available SRAM address at power on. Uses the
 * serial module to print out the read data. Visual inpsection is
 * is used here.
 *
 */
void unit_test_0001(void)
{
    const int UT_NUM = 1;
    volatile uint8_t data = (uint8_t) 0;
    char buffer[100];

    for (int i = 0; i < 16 /* 4 address bits = 16 addresses*/; i++)
    {
      delay(500);
      read_sram_address(((uint8_t) i), &data);

      memset(buffer, 0, sizeof(buffer));
      sprintf(buffer, "INFO (%02d) - Address: %02d -- Data: 0x%02x\n\0", UT_NUM, i, data);
      Serial.print(buffer);
      data = (uint8_t) 0;
    }
} /* unit_test_0001 */

/** @fn void unit_test_0002(void)
 * @brief Writes all 0 to addressable portions of SRAM.
 */
void unit_test_0002(void)
{
    const int UT_NUM = 2;
    volatile uint8_t data = (uint8_t) 0;
    char buffer[100];

    for (int i = 0; i < 16 /* 4 address bits = 16 addresses*/; i++)
    {
      delay(750);
      write_sram_address(((uint8_t) i), ((uint8_t) 0));
      delayMicroseconds(1);
      read_sram_address(((uint8_t) i), &data);


      memset(buffer, 0, sizeof(buffer));

      if (data == ((uint8_t) 0))
      {
        sprintf(buffer, "INFO (%02d) - Address: %02d -- Data: 0x%02x\n\0", UT_NUM, i, data);
      }

      else
      {
        sprintf(buffer, "ERR! (%02d) - Address: %02d -- Data: 0x%02x\n\0", UT_NUM, i, data);
      }

      Serial.print(buffer);
    }
} /* unit_test_0002 */

/** @fn void unit_test_0003(void)
 * @brief Writes all sequential values to addressable portions of SRAM.
 */
void unit_test_0003(void)
{
    const int UT_NUM = 3;
    volatile uint8_t data = (uint8_t) 0;
    char buffer[100];

    for (int i = 0; i < 16 /* 4 address bits = 16 addresses*/; i++)
    {
      delay(750);
      write_sram_address(((uint8_t) i), ((uint8_t) i));
      delayMicroseconds(1);
      read_sram_address(((uint8_t) i), &data);


      memset(buffer, 0, sizeof(buffer));

      if (data == ((uint8_t) i))
      {
        sprintf(buffer, "INFO (%02d) - Address: %02d -- Data: 0x%02x\n\0", UT_NUM, i, data);
      }

      else
      {
        sprintf(buffer, "ERR! (%02d) - Address: %02d -- Data: 0x%02x\n\0", UT_NUM, i, data);
      }

      Serial.print(buffer);
      data = (uint8_t) 0;
    }
} /* unit_test_0003 */
