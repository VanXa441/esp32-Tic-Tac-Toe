# ESP32 MicroPython Multiplayer Tic-Tac-Toe Server

A lightweight, hardware-hosted multiplayer Tic-Tac-Toe web application built on an ESP32 microcontroller using raw MicroPython HTTP socket programming.

## Features
* **Zero Frameworks:** Uses raw MicroPython TCP sockets (`socket` library) to serve HTTP requests.
* **Access Point Hosting:** Creates its own Wi-Fi Access Point (`test`).
* **Real-Time Dual-Client Lobby:** Tracks client IP connections and dynamically pairs two devices.
* **REST-like Sync Polling:** Uses JavaScript `fetch()` API polling to synchronize board moves, active player turns, and game states (`WIN_P1`, `WIN_P2`, `DRAW`, `PLAYING`).
* **Memory Optimization:** Uses explicit garbage collection (`gc.collect()`) to reliably handle recurring polling traffic on microcontrollers.

## How to Flash & Run

1. **Flash MicroPython:** Load MicroPython firmware onto your ESP32 board.
2. **Upload Code:** Upload `esp32-Tic-Tac_Toe` to the ESP32 root filesystem using **Thonny**, **ampy**, or **mpremote**.
3. **Connect Devices:** 
   * Power on the ESP32.
   * Connect two mobile phones or laptops to the Wi-Fi network `test`.
   * Open `http://192.168.4.1:8080` in a web browser on both devices.
