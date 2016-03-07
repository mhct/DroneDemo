import os

file_list = [f for f in os.walk(".").next()[2] if f.startswith("Cell")]

print file_list