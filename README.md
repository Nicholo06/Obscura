# Obscura: Chrome Extension Obfuscation Tool

**Obscura** is a simple Python wrapper designed to automate the obfuscation and packaging of Chrome Extension source code. It handles the repetitive tasks of running the obfuscator, maintaining folder structures, and creating production-ready zip files.

---

## Who is this for?

This tool is built for **developers in the early testing and distribution phases** of their extension. It is ideal for those who:
- Want to share their progress with beta testers without exposing the raw source code.
- Need a quick, "one-click" way to package their extension for manual installation (unpacked mode).
- Want to protect proprietary logic or API endpoints from casual inspection during the development lifecycle.

---

## The Purpose of Obscura

The real use of this tool is **convenience**. Instead of manually running terminal commands for every file, Obscura:
1.  **Protects Your Privacy:** Quickly scrambles your JavaScript so it isn't easily readable by others during early testing.
2.  **Saves Time:** Automates the "Obfuscate -> Copy Assets -> Rename Folder -> Zip" workflow into a single command.
3.  **Ensures Compatibility:** Uses pre-set flags specifically chosen to keep extensions functional under Chrome's Manifest V3 security rules.

---

## Features

- **Automated Workflow:** Walks through your folder, obfuscates `.js` files, and copies all other assets (HTML, CSS, JSON, Images) as-is.
- **MV3 Compliant:** Specifically disables the `self-defending` flag to prevent CSP violations in Chrome Extensions.
- **Clean UI:** Includes a simple terminal interface with a progress bar and project detection.
- **Ready to Ship:** Outputs a sanitized folder and an `extension_ship.zip` file automatically.

---

## Requirements

1. **Node.js:** Required for the underlying obfuscation engine.
2. **Obfuscation Engine:** Install the core engine globally:
   ```bash
   npm install -g javascript-obfuscator
   ```
3. **Python 3:** Required to run the `obfuscate.py` script.

---

## How to Use

1.  **Prepare:** Place your readable extension code into the `src/` folder.
2.  **Run:** Open your terminal in the project directory and run:
    ```bash
    python obfuscate.py
    ```
3.  **Confirm:** Verify the detected project name and type `y` to start.
4.  **Result:** Your protected code will be generated in a new folder (named after your project) and a zip file.

---

## Important Notes

- **Early Testing Tool:** This is intended for protection during early stages. For high-security production releases, always review the obfuscation settings in `obfuscate.py`.
- **Debug First:** Obfuscated code is nearly impossible to debug. Ensure your extension is 100% functional in the `src/` folder before running this script.
- **CSP Compliance:** The `self-defending` flag is disabled by default because it uses `eval()`, which is prohibited in Chrome Extensions.

---

