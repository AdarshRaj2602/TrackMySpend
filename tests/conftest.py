import os
import sys

Project_root = os.path.join(os.path.dirname(__file__), "..")
print("Project_root", Project_root)
sys.path.insert(0, Project_root)
print("sys.path", sys.path)