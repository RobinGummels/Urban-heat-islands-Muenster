#!/usr/bin/env python3
import os
import sys
import subprocess

def run_script(script_name):
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    print(f"[*] Running {script_name} ...")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] Fehler in {script_name}:\n{result.stderr}")
        sys.exit(result.returncode)
    else:
        print(f"[+] {script_name} completed successfully.\n")

def main():
    # Reihenfolge der Skripte
    scripts = [
        "clip_and_convert_to_LST.py",
        "compute_seasonal_means.py",
        "normalize_seasonal_means_z-trans.py",
        "boxplot_by_class.py",
        "z_transformed_boxplot_by_class.py",
        "correlate_lst_with_indices.py",
        "deltaZ-statistics.py"
    ]

    for script in scripts:
        run_script(script)

    print("[*] Full analysis finished. Alle Ergebnisse liegen nun in den entsprechenden Ordnern.")

if __name__ == "__main__":
    main()
