import os
import shutil
import frontmatter
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='Update Quartz content from Obsidian vault.')
parser.add_argument('--vault', action="store", required=True, help='Obsidian vault path')
parser.add_argument('--content', action="store", required=True, help='Quartz content path')
parser.add_argument('--cleanup', action="store_true", default=False, help='Remove files from Quartz content that do not get copied')
args = parser.parse_args()

obsidian_vault_path = args.vault
quartz_content_path = args.content
included_dirs = [
	'self',
	'website-other',
]

# create Quartz content directory for Obsidian notes if it doesn't exist
os.makedirs(quartz_content_path, exist_ok=True)

def is_published(file_path):
	with open(file_path, 'r', encoding='utf-8') as file:
		post = frontmatter.load(file)
		return post.get('published', False) == True
	
for root, dirs, files in os.walk(obsidian_vault_path):
	# exclude directories listed in excluded_dirs
	dirs[:] = [d for d in dirs if d in included_dirs]
	
	rel_obsidian_dir = os.path.relpath(root, obsidian_vault_path)
	destination_dir = os.path.join(quartz_content_path, rel_obsidian_dir)

	copied_files = []
	for file in files:
		if file.endswith('.md'):
			abs_obsidian_path = os.path.join(root, file)
			if is_published(abs_obsidian_path):
				Path(destination_dir).mkdir(parents=True, exist_ok=True)

				destination_path = os.path.join(destination_dir, file)
				print("Copying " + abs_obsidian_path + " to " + destination_path)
				shutil.copy2(abs_obsidian_path, destination_path)
				copied_files.append(file)
	
	if args.cleanup:
		# remove files that were not copied
		for file in os.listdir(destination_dir):
			if file not in copied_files:
				file_path = os.path.join(destination_dir, file)
				if os.path.isfile(file_path):
					print("REMOVE:", file_path)
					os.remove(file_path)