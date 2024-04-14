from _setup_deps import Version, Normal_People_Date, init_description, get_y_n, parse_notes, clear_screen

from setuptools import setup
import shutil
import time
import sys
import os



IS_CALLED_BY_PIP = False

ENV_STR = ""
for item in os.environ:
	ENV_STR += f"{item}={os.environ[item]}"
if "PIP" in ENV_STR.upper():
	IS_CALLED_BY_PIP = True



NOTES = "\n"
NOTES += "Initial release.\n"

CURRENT_VERSION = Version(
	date=Normal_People_Date(14, 4, 2024),
	version_number="0.1",
	notes=parse_notes(NOTES)
)
CURRENT_VERSION.validate()

LONG_DESCRIPTION = init_description()
LONG_DESCRIPTION += f"\n## V{CURRENT_VERSION.version_number} released on {CURRENT_VERSION.repr_date()}\n"
LONG_DESCRIPTION += NOTES



if not os.getcwd().endswith("routput"):
	raise Exception("This script must be run from the root of the project directory.")



simple_path_checks = ["/routput/__init__.py"]
if not all(os.path.exists(os.path.abspath(os.getcwd()+p)) for p in simple_path_checks):
	raise Exception("This script must be run from the root of the project directory.")


if not IS_CALLED_BY_PIP:
	print("WARNING: ABOUT TO REMOVE THE `dist` DIRECTORY!!")
	has_backed_up = get_y_n("Have you backed up the project? (y/n) ")
	if not has_backed_up:
		exit(0)
else:
	print("\n\n\nWARNING: ABOUT TO DELETE THE `dist` DIRECTORY!!")
	print("YOU HAVE 5 SECONDS TO CANCEL THIS OPERATION.")
	time.sleep(5)
shutil.rmtree("dist", ignore_errors=True)



if len(sys.argv) == 1:
	sys.argv.append("bdist_wheel")



setup(
	name="routput",
	version=CURRENT_VERSION.version_number,
	keywords=[
		"python",
		"recursive",
		"find",
		"files",
		"directories",
		"subdirectories",
		"contents",
		"recursive output",
		"routput"
	],
	author="matrikater (Joel C. Watson)",
	author_email="matrikater@matriko.xyz",
	description="Find files recursively and optionally print their contents.",
	long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
	long_description=LONG_DESCRIPTION,
	classifiers=[
		"Development Status :: 3 - Alpha",
		"Programming Language :: Python :: 3",
		"Natural Language :: English",
	],
)



if IS_CALLED_BY_PIP:
	exit(0)



print("\n] Setup complete.\n\n")
input("Press Enter to continue... ")
clear_screen()

print("Please review the following information before publishing:")
print(f"\tRelease Date: {CURRENT_VERSION.repr_date()}")
print(f"\tVersion Number: {CURRENT_VERSION.version_number}")
print(f"\tRelease Notes: \"{CURRENT_VERSION.notes}\"")
print(f"\tDescription is readable below...\n{LONG_DESCRIPTION}")

print()
did_check_version = get_y_n("Did you update the version information? (y/n) ")
if not did_check_version:
	exit(0)



do_publish = get_y_n("Would you like to publish to PyPi? (y/n) ")
if not do_publish:
	exit(0)

again_to_be_sure = get_y_n("ARE YOU SURE? Remember, you can't unpublish. (y/n) ")
if not again_to_be_sure:
	exit(0)

TOKEN = None
if os.path.exists(".token"):
	with open(".token", "r") as f:
		TOKEN = f.read().strip()
if TOKEN is None:
	def get_tok() -> str:
		t = input("Enter your PyPi token: ")
		if not get_y_n("Please confirm. Is it correct? (y/n) "):
			return get_tok()
		return t
	TOKEN = get_tok()
	with open(".token", "w") as f:
		f.write(TOKEN)

os.system(f"python3.12 -m twine upload --verbose --repository pypi -p \"{TOKEN}\" dist/*")