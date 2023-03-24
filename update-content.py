import os
import shutil
import frontmatter
from pathlib import Path

obsidian_vault_path = "/home/greg/brain"
quartz_content_path = "/home/greg/quartz/content"
included_dirs = [
	'self',
	'website-other',
]

# remove everything in the destination directory
if os.path.exists(quartz_content_path):
    shutil.rmtree(quartz_content_path)

# create Quartz content directory for Obsidian notes if it doesn't exist
os.makedirs(quartz_content_path, exist_ok=True)

def is_published(file_path):
	with open(file_path, 'r', encoding='utf-8') as file:
		post = frontmatter.load(file)
		return post.get('published', False) == True
	
for root, dirs, files in os.walk(obsidian_vault_path):
	# exclude directories listed in excluded_dirs
	dirs[:] = [d for d in dirs if d in included_dirs]
	
	for file in files:
		if file.endswith('.md'):
			abs_obsidian_path = os.path.join(root, file)
			if is_published(abs_obsidian_path):
				rel_obsidian_dir = os.path.relpath(root, obsidian_vault_path)
				print("rel:", rel_obsidian_dir)

				destination_dir = os.path.join(quartz_content_path, rel_obsidian_dir)
				Path(destination_dir).mkdir(parents=True, exist_ok=True)

				destination_path = os.path.join(destination_dir, file)
				print("Copying " + abs_obsidian_path + " to " + destination_path)
				shutil.copy2(abs_obsidian_path, destination_path)