# LTC6904-Programmable-Oscillator-Control
This project provides a complete solution for controlling the LTC6904 programmable oscillator using an ESP32 via the I2C protocol. It is specifically designed for radio frequency (RF) applications, such as replacing crystals in vintage radios or generating precise clock signals from 1 kHz to 68 MHz.


# LTC6904 Programmable Oscillator Control via ESP32

This project provides a complete solution for controlling the **LTC6904** programmable oscillator using an **ESP32** via the **I2C** protocol. Ideal for RF applications, such as replacing crystals in vintage radios (e.g., Southcom 130) or generating precise clock signals from **1 kHz to 68 MHz**.

## 🛠️ Hardware Specifications

### 1. Pinout Mapping
The **LTC6904** is the I2C version (not to be confused with the SPI-based LTC6903). Both AD1 and AD2 must be grounded to set the default I2C address.

| LTC6904 Pin | Function | ESP32 / Circuit Connection |
| :--- | :--- | :--- |
| **1** | **GND** | Common Ground |
| **2** | **AD2** | GND (Sets I2C Address to `0x17`) |
| **3** | **SCL** | GPIO 22 |
| **4** | **SDA** | GPIO 21 |
| **5** | **AD1** | GND (Sets I2C Address to `0x17`) |
| **6** | **CLK** | **RF Signal Output** |
| **7** | **CLK** | No Connection (Inverted Output) |
| **8** | **VCC** | **3.3V DC** (Do NOT use 5V) |

### 2. Required Components & Values
To ensure signal stability and clean RF injection, the following components are required:

* **C1 (Decoupling):** `0.1µF` ceramic capacitor between Pin 8 and Pin 1.
* **C2 (DC Block):** `470pF` ceramic capacitor in series with Pin 6.
* **R1 (Attenuator):** `4.7kΩ` resistor in series after C2 (adjust this value to control signal strength into the radio).

---
🟢 Added: I2C Pull-Up Resistors RequirementThe LTC6904 uses an open-drain I2C bus. This means the chip can only pull the lines LOW; it cannot pull them HIGH. Therefore, you must add two pull-up resistors to the SDA and SCL lines for the communication to work.Values: Use 4.7kΩ resistors (standard for 400kHz I2C).Connection: * One resistor from SDA (GPIO 21) to 3.3V.One resistor from SCL (GPIO 22) to 3.3V.Note: Some ESP32 development boards (like some versions of the DevKit V1) have internal pull-ups that can be enabled via software, but for RF stability and reliable I2C switching, external physical resistors are strongly recommended.Actualización del Diagrama de Conexiones (Markdown Table)LTC6904 PinFunctionConnection3SCLGPIO 22 + 4.7kΩ Resistor to 3.3V4SDAGPIO 21 + 4.7kΩ Resistor to 3.3V
## 🖥️ Frequency Configuration Utility

The chip requires a specific 16-bit configuration (4 bits for the Octave, 10 bits for the DAC, and 2 bits for the Output mode). 

### How to use the Calculator:
1.  Open the included `LTC6904_Calculator.html` in your browser.
2.  Type your target frequency (e.g., `12.697`).
3.  Copy the generated **MSB** and **LSB** Hex values.

> **Note:** If the calculator seems stuck on low frequencies, clear your browser cache or rename the HTML file.

---

## 💻 ESP32 Firmware (Arduino)

Copy this code into the Arduino IDE. Replace `regMSB` and `regLSB` with the values from the calculator.

```cpp
#include <Wire.h>

// I2C Address when AD1/AD2 are grounded
const int LTC_ADDR = 0x17; 

// --- GENERATED VALUES FROM CALCULATOR ---
byte regMSB = 0xCA;  // Example for 12.697 MHz
byte regLSB = 0xB5;  // Example for 12.697 MHz
// -----------------------------------------

void setup() {
  Wire.begin(21, 22); // Initialize I2C (SDA, SCL)
  Serial.begin(115200);
  
  delay(1000);
  Serial.println("Programming LTC6904...");

  Wire.beginTransmission(LTC_ADDR);
  Wire.write(regMSB); 
  Wire.write(regLSB);
  
  if (Wire.endTransmission() == 0) {
    Serial.println("Success: Frequency Loaded.");
  } else {
    Serial.println("Error: Device not found.");
  }
}

void loop() {
  // Output is stable once programmed.
}
```

---

## ⚠️ Implementation Checklist

- [ ] **Voltage Check:** Ensure the LTC6904 is powered by **3.3V**. 5V will damage the chip.
- [ ] **I2C Pull-ups:** If your ESP32 board doesn't have them, add $4.7k\Omega$ resistors from SDA and SCL to 3.3V.
- [ ] **Filtering:** Never inject the signal directly without the `470pF` capacitor to avoid sending DC current into the radio's mixer.
- [ ] **Address Check:** If the serial monitor says "Device not found", verify that Pins 2 and 5 are strictly connected to GND.

---
