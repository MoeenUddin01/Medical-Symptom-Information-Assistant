import os
import sys

# Ensure python can resolve the root 'backend' module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app
