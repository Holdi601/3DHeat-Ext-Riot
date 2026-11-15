import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# The tests never ask GitHub for a newer release.
os.environ["HEAT3D_NO_UPDATE"] = "1"
