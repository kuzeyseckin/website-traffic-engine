# 🚀 Playwright Async Web Traffic Simulator

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Playwright](https://img.shields.io/badge/Playwright-Async-green?style=for-the-badge&logo=playwright)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-informational?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

A high-performance, asynchronous desktop application built with **Python**, **Playwright**, and **CustomTkinter** to simulate realistic web visits. Engineered with a strict resource interceptor to minimize proxy bandwidth consumption while maintaining natural user behavior.

---

## ✨ Key Features

* **⚡ Asynchronous Worker Queue:** Powered by `asyncio.Queue` to manage multiple concurrent browser contexts without freezing the GUI thread.
* **🛡️ Strict Bandwidth Optimization:** Built-in `TrafficInterceptor` aborts heavy resources (`image`, `media`, `font`, `stylesheet`, `websocket`) and blocks 25+ major ad/tracking networks (DoubleClick, Taboola, Analytics, etc.) to save residential/mobile proxy data.
* **🔄 Multi-Format Proxy Parser:** Automatically detects and parses `ip:port`, `ip:port:user:pass`, and `user:pass@ip:port` formats.
* **🕵️ Anti-Detect & Fingerprint Randomization:**
  * Dynamic User-Agent generation via `fake-useragent`.
  * Randomized screen viewports, locales (`en-US`, `en-GB`, `tr-TR`, `de-DE`), and timezones.
  * Randomized HTTP `Referer` headers (Google, Reddit, X/Twitter).
  * `navigator.webdriver` spoofing.
* **🖱️ Human-Like Interaction:** Simulates natural page dwelling and randomized vertical scrolling.
* **🖥️ Modern GUI:** Clean, responsive Dark/Light mode interface built with `CustomTkinter` featuring real-time status logging.

---

## 📂 Project Structure

```text
traffic_simulator/
│
├── core/
│   ├── __init__.py
│   ├── proxy_parser.py       # Parses raw proxy strings into Playwright dict format
│   ├── interceptor.py        # Request interception & bandwidth saving rules
│   └── engine.py             # Async Playwright engine, worker queue & page actions
│
├── ui/
│   ├── __init__.py
│   └── app.py                # CustomTkinter GUI implementation
│
├── main.py                   # Application entry point
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

---

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/playwright-traffic-simulator.git](https://github.com/YOUR_USERNAME/playwright-traffic-simulator.git)
   cd playwright-traffic-simulator
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright Chromium browser binaries:**
   ```bash
   playwright install chromium
   ```

---

## 🚀 Usage

1. Run the application from the root directory:
   ```bash
   python main.py
   ```
2. **Target URL:** Enter the full destination URL (e.g., `https://example.com`).
3. **Proxy List:** Paste your proxies (one per line). Supported formats:
   * `192.168.1.1:8080`
   * `192.168.1.1:8080:username:password`
   * `username:password@192.168.1.1:8080`
4. **Configuration:**
   * **Time Spent on Page:** Duration (in seconds) each tab stays active after scrolling.
   * **Maximum Concurrent Tabs:** Number of simultaneous browser contexts.
   * **Cycles:** How many times the entire proxy list should be repeated.
   * **Headless Mode:** Run browsers in the background without visible windows.
5. Click **Start the Simulator** and monitor real-time task execution in the **Status Report** console.

---

## ⚠️ Disclaimer

This tool is developed strictly for **educational purposes, stress testing, and analyzing server/proxy bandwidth behavior** on websites you own or have explicit permission to test. The author is not responsible for any misuse or violation of third-party Terms of Service.
