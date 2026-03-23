import os
import shutil
import subprocess
import zipfile
import time
import json
import sys

# --- Configuration ---
SOURCE_DIR = "./src"
OUTPUT_DIR = "./dist"
ZIP_NAME = "extension_ship.zip"

# Obfuscation Settings for Manifest V3 (Security & Compliance)
OBFUSCATION_FLAGS = [
    "--compact", "true",
    "--string-array", "true",
    "--string-array-encoding", "base64",
    "--string-array-threshold", "0.80",
    "--identifier-names-generator", "hexadecimal",
    "--rename-globals", "false",
    "--self-defending", "false", 
    "--control-flow-flattening", "true",
    "--control-flow-flattening-threshold", "0.5"
]

class ObfuscatorCLI:
    def __init__(self):
        self.stats = {"obfuscated": 0, "copied": 0, "errors": 0}
        self.project_name = "Unknown Project"
        self.tool_cmd = None

    def print_status(self, current, total, filename):
        """Updates the progress bar and current file status on a single line."""
        bar_length = 30
        progress = float(current) / total
        block = int(round(bar_length * progress))
        
        display_name = (filename[:35] + '...') if len(filename) > 38 else filename.ljust(38)
        bar = "█" * block + "-" * (bar_length - block)
        percent = int(progress * 100)
        
        status = f"\r    [{bar}] {percent}% | {current}/{total} | Processing: {display_name}"
        sys.stdout.write(status)
        sys.stdout.flush()

    def get_project_name(self):
        """Recursively searches for manifest.json and extracts the project name."""
        for root, _, files in os.walk(SOURCE_DIR):
            if "manifest.json" in files:
                manifest_path = os.path.join(root, "manifest.json")
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        content = ""
                        for line in f:
                            if not line.strip().startswith("//"):
                                content += line
                        
                        data = json.loads(content)
                        name = data.get("name")
                        if name:
                            return name
                except Exception:
                    continue
        return "Unknown Extension"

    def check_env(self):
        """Verify obfuscation engine is installed."""
        cmd = "javascript-obfuscator.cmd" if os.name == 'nt' else "javascript-obfuscator"
        try:
            subprocess.run([cmd, "--version"], capture_output=True, check=True)
            self.tool_cmd = cmd
            return True
        except:
            print("\n    Error: 'javascript-obfuscator' not found.")
            print("    Please run: npm install -g javascript-obfuscator")
            return False

    def run(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        ascii_art = r"""
    ____  _                              
   / __ \| |                             
  | |  | | |__  ___  ___ _   _ _ __ __ _ 
  | |  | | '_ \/ __|/ __| | | | '__/ _` |
  | |__| | |_) \__ \ (__| |_| | | | (_| |
   \____/|_.__/|___/\___|\__,_|_|  \__,_|
        """
        print(ascii_art)

        if not self.check_env(): return

        if not os.path.exists(SOURCE_DIR) or not os.listdir(SOURCE_DIR):
            print(f"    Source directory '{SOURCE_DIR}' is empty.")
            print("    Please drop your extension source code into the 'src' folder.")
            os.makedirs(SOURCE_DIR, exist_ok=True)
            return

        self.project_name = self.get_project_name()
        print(f"    Project Detected: {self.project_name}")
        
        confirm = input(f"\n    Obfuscate this project? (y/n): ").lower()
        if confirm != 'y': 
            print("    Build cancelled.")
            return

        print("\n    Initializing build sequence...")
        if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        all_files = []
        for root, _, files in os.walk(SOURCE_DIR):
            for f in files:
                all_files.append(os.path.join(root, f))
        
        total = len(all_files)
        start_time = time.time()

        for i, src_file in enumerate(all_files, 1):
            rel_path = os.path.relpath(src_file, SOURCE_DIR)
            dest_file = os.path.join(OUTPUT_DIR, rel_path)
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)

            self.print_status(i, total, rel_path)

            if src_file.endswith(".js"):
                try:
                    subprocess.run(
                        [self.tool_cmd, src_file, "--output", dest_file] + OBFUSCATION_FLAGS,
                        capture_output=True, text=True, check=True
                    )
                    self.stats["obfuscated"] += 1
                except:
                    self.stats["errors"] += 1
            else:
                shutil.copy2(src_file, dest_file)
                self.stats["copied"] += 1

        print(f"\n\n    Finalizing: Creating {ZIP_NAME}...")
        try:
            with zipfile.ZipFile(ZIP_NAME, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(OUTPUT_DIR):
                    for f in files:
                        fp = os.path.join(root, f)
                        zipf.write(fp, os.path.relpath(fp, OUTPUT_DIR))
        except Exception as e:
            print(f"    Zip Error: {e}")

        sanitized_name = "".join([c if c.isalnum() or c in (' ', '-', '_') else '' for c in self.project_name]).strip().replace(' ', '_')
        if not sanitized_name or sanitized_name.lower() == "unknown_extension":
            sanitized_name = "obfuscated_extension"
        
        final_output_path = os.path.join(os.path.dirname(OUTPUT_DIR), sanitized_name)
        
        try:
            if os.path.exists(final_output_path) and os.path.abspath(final_output_path) != os.path.abspath(OUTPUT_DIR):
                shutil.rmtree(final_output_path)
            os.rename(OUTPUT_DIR, final_output_path)
        except Exception as e:
            print(f"\n    Could not rename folder to '{sanitized_name}': {e}")
            final_output_path = OUTPUT_DIR

        elapsed = time.time() - start_time
        print("\n    " + "="*40)
        print(f"    BUILD COMPLETE in {elapsed:.1f}s")
        print(f"    - JS Files Protected: {self.stats['obfuscated']}")
        print(f"    - Asset Files Moved:  {self.stats['copied']}")
        print(f"    - Output Folder:      {final_output_path}")
        print(f"    - Ready to Ship:      {ZIP_NAME}")
        print("    " + "="*40)

if __name__ == "__main__":
    try:
        ObfuscatorCLI().run()
    except KeyboardInterrupt:
        print("\n\n    Aborted by user.")
        sys.exit(0)
