import sys

def remove_duplicate_empty_lines(lines:"list[str]") -> "str":
	new_lines = []
	for line in lines:
		if line.strip() == "":
			if new_lines and new_lines[-1].strip() == "":
				continue
		new_lines.append(line)
	return "".join(new_lines)

starting_directory = sys.argv[1]
item_path = sys.argv[2]
index = sys.argv[3]

with open(item_path, "r") as f:
	lines = f.readlines()

print(f"[{index}] '{item_path}': ```\n")
print(remove_duplicate_empty_lines(lines))
print("\n```")
