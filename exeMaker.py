import sys
from cx_Freeze import setup, Executable

setup(
		name="Demo",
		version="1.0",
		description = "client file",
		author = "tear94fall",
		executables = [Executable("Client.py")])