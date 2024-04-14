#!/usr/bin/env python3



import os
import argparse
import subprocess
from sys import argv as SYS_ARGV
from dataclasses import dataclass

@dataclass
class Validated_Arguments:
	starting_directory: str
	extensions_list: list[str]
	include_list: list[str]
	ignore_list: list[str]
	do_print_structure: bool
	do_protect_privacy: bool
	do_print: bool
	do_use_bat: bool
	do_use_color: bool



if os.name == "nt":
	SPLITTER = "\\"
else:
	SPLITTER = "/"



def display_error(err_msg):

	if os.name != "nt":
		err_msg = f"\033[31m{err_msg}\033[0m"

	print(err_msg)
	exit(1)

	return None

	f"END {display_error}"



def parse_bracket_list(s):

	return s[1:-1].replace(" ", "").split(",") if s.startswith("[") and s.endswith("]") else []

	f"END {parse_bracket_list}"



def print_structure(directory):
	indent_level = 0
	for root, _, _ in os.walk(directory):

		indent_level = root[len(directory):].count(os.sep)
		indent = "\t" * indent_level

		print(f"{indent}+-- {os.path.basename(root)}/", flush=True)

	return None

	f"END {print_structure}"



def __x__is_in_ignore_list(full_path:"str", ignore_list:"list[str]") -> "bool":
	"""
	Will check if the full_path is in the ignore_list.
	This works if x item in ignore_list is only the name AND if it is the full path.
	"""
	assert os.path.isabs(full_path)
	for item in ignore_list:

		num_item_sections = len(item.split(SPLITTER))

		if item == full_path:
			return True

		elif item == full_path.split(SPLITTER)[-num_item_sections:]:
			return True

	return False
	f"END {__x__is_in_ignore_list}"

def find_children_of_starting_dir(starting_directory, extensions_list, include_list, ignore_list) -> "list[str]":
	"""
	Will find all the files in the starting_directory that have the extensions in the extensions_list.
	"""
	found_items = []
	for root, dirs, files in os.walk(starting_directory):

		for dir in dirs:
			full_path = os.path.join(root, dir)
			if __x__is_in_ignore_list(full_path, ignore_list):
				for s, _, f in os.walk(full_path):
					for file in f:
						full_path = os.path.join(s, file)
						if __x__is_in_ignore_list(full_path, ignore_list):
							continue
						ignore_list.append(full_path)

		for file in files:
			full_path = os.path.join(root, file)
			if __x__is_in_ignore_list(full_path, ignore_list):
				continue
			if file.endswith(tuple(extensions_list)) or file in include_list:
				found_items.append(full_path)

	for item in found_items:
		assert os.path.exists(item)
		assert os.path.isabs(item)
	return found_items
	f"END {find_children_of_starting_dir}"



def use_bat_to_print(starting_directory, file_path, i, do_protect_privacy):
	# TODO: Add support for `do_protect_privacy` in this function.
	try:

		subprocess.run(["bat", "--paging=never", file_path])

	except Exception as e:

		display_error(f"Could not use bat: {e}")

	return None
	f"END {use_bat_to_print}"

def normal_print(starting_directory, item_path, i, do_protect_privacy):

	if os.path.isdir(item_path):
		return
	
	with open(item_path, "r") as f:
		if do_protect_privacy:
			item_path = item_path[len(starting_directory):]
		print(f"[{i}] '{item_path}': ```\n")
		print(f.read())
		print("\n```")
	
	return None
	f"END {normal_print}"



def validate_args(args):

	if not os.path.exists(args.starting_directory):
		display_error(f"[[routput.py]]: Invalid `starting_directory`: [{args.starting_directory}]\nDirectory does not exist.")

	starting_dir = os.path.abspath(args.starting_directory)
	extensions_list = [ext if ext.startswith('.') else f".{ext}" for ext in parse_bracket_list(args.extensions)]
	include_list = parse_bracket_list(args.also_include)
	ignore_list = parse_bracket_list(args.ignore)

	for i, item in enumerate(ignore_list):
		if item == "":
			ignore_list.pop(i)
			continue
		if not os.path.exists(item):
			display_error(f"[[routput.py]]: Invalid `ignore_list` item: [{item}]\nItem does not exist.")
		ignore_list[i] = os.path.abspath(item)

	for i, item in enumerate(include_list):
		if item == "":
			include_list.pop(i)
			continue
		if not os.path.exists(item):
			display_error(f"[[routput.py]]: Invalid `also_include` item: [{item}]\nItem does not exist.")
		include_list[i] = os.path.abspath(item)

	return Validated_Arguments(
		starting_directory= 	starting_dir,
		extensions_list= 	extensions_list,
		include_list= 		include_list,
		ignore_list= 		ignore_list,
		do_print_structure= 	args.do_print_structure,
		do_protect_privacy= 	args.do_protect_privacy,
		do_print= 		not args.no_print,
		do_use_bat= 		args.do_use_bat,
		do_use_color= 		args.do_colors
	)

	f"END {validate_args}"



def main():

	parser = argparse.ArgumentParser(description="Find files based on their extensions, recursively from a starting directory.")
	
	parser.add_argument("-d", "--starting-directory", type=str, default=".", help="Directory to start the search from.")
	parser.add_argument("-s", "--do-print-structure", action="store_true", default=False, help="Print the directory structure.")
	parser.add_argument("-e", "--extensions", type=str, default="[c,h]", help="List of file extensions to search for, in the format [ext1,ext2,...].")
	parser.add_argument("-p", "--do-protect-privacy",  action="store_true", default=False, help="Anonymize the file paths to be relative to the starting directory.")
	parser.add_argument("-a", "--also-include", type=str, default="[]", help="List of additional filenames to include, in the format [file1,file2,...].")
	parser.add_argument("-i", "--ignore", type=str, default="[]", help="List of filenames to ignore, in the format [file1,file2,dir1,dir2...].")
	parser.add_argument("-n", "--no-print", action="store_true", default=False, help="Don't print the files, just return them.")
	parser.add_argument("-b", "--do-use-bat", action="store_true", default=False, help="Use `bat` utility for syntax highlighting.")
	parser.add_argument("-c", "--do-colors", action="store_true", default=False, help="Use a different color for each file.")
	
	if not len(SYS_ARGV) > 1:
		parser.print_help()
		exit(0)

	args = parser.parse_args()
	args = validate_args(args)
	
	for i, item in enumerate(args.ignore_list):
		print(f"Ignoring: [{item}]")

	if args.do_print_structure:
		print("Directory Structure:")
		print_structure(args.starting_directory)
	
	found_items = find_children_of_starting_dir(
		args.starting_directory,
		args.extensions_list,
		args.include_list,
		args.ignore_list
	)
	
	for i, item_path in enumerate(found_items):
		if args.do_print:
			if args.do_use_bat:
				use_bat_to_print(args.starting_directory, item_path, i, args.do_protect_privacy)
			else:
				normal_print(args.starting_directory, item_path, i, args.do_protect_privacy)
		else:
			path = item_path
			if args.do_protect_privacy:
				path = "." + path[len(args.starting_directory):]
				assert os.path.exists(path)
			print(f"[{i}] '{path}'")
	
	return None
	f"END {main}"



if __name__ == "__main__":
	main()
