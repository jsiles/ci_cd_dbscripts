import os
from datetime import datetime

REPO_PATH = "./scripts"
OUTPUT_SCRIPT = f"deploy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

with open(OUTPUT_SCRIPT, "w", encoding="utf-8") as out:
    for root, dirs, files in os.walk(REPO_PATH):
        for file in sorted(files):
            if file.endswith(".sql"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    out.write(f"-- Script: {file}\n")
                    out.write(f.read() + "\n/\n")

print(f"✅ Script consolidado generado: {OUTPUT_SCRIPT}")
