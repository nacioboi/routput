import os, sys
sys.path.append(os.path.abspath('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/'))

from templated_setup import templated_setup

DESC = """
recursively searches for files based on their extensions starting from a specified directory. It can print the directory structure, include or exclude specific files, use syntax highlighting for output, and anonymize file paths for privacy.
"""

templated_setup.Setup_Helper.init(".templated_setup.cache.json")
templated_setup.Setup_Helper.setup(
	name= "routput",
	author="matrikater (Joel Watson)",
	description=DESC.strip(),
	install_requires=[f"templated-setup"],
)
