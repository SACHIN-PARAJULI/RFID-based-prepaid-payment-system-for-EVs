#include <MFRC522v2.h>
#include <MFRC522DriverSPI.h>
#include <MFRC522DriverPinSimple.h>
#include <MFRC522Debug.h>


MFRC522DriverPinSimple ss_pin(2); //D4 // Configurable, see typical pin layout above.

MFRC522DriverSPI driver{ss_pin}; // Create SPI driver.

MFRC522 mfrc522{driver};  // Create MFRC522 instance.
