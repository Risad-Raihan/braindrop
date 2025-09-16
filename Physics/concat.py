import os
from pathlib import Path

# Set your directory path
md_dir = Path('/home/risad/projects/physics_embedding/Physics/')

# Create output content
combined_content = []

# Process files in order (1-13)
for i in range(1, 14):
    file_path = md_dir / f'chapter_{i:02d}.md'
    
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            combined_content.append(f"# Chapter {i}\n\n{content}\n\n")
            print(f"Added: {file_path.name}")
    else:
        print(f"File not found: {file_path.name}")

# Write combined file
output_path = md_dir / 'combined_physics.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(combined_content))

print(f"\nCombined file created: {output_path}")