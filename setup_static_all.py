import shutil
import os

# Copy your 4 healthy and 4 diseased leaf images into the static folders
healthy_src = ['leaf1.jpg', 'leaf2.jpg', 'leaf3.jpg', 'leaf4.jpg']
diseased_src = ['leaf1.jpg', 'leaf2.jpg', 'leaf3.jpg', 'leaf4.jpg']

if not os.path.exists('static/healthy'):
    os.makedirs('static/healthy')
if not os.path.exists('static/diseased'):
    os.makedirs('static/diseased')

for f in healthy_src:
    shutil.copy(f, 'static/healthy/' + f)

for f in diseased_src:
    shutil.copy(f, 'static/diseased/' + f)

print("All images copied successfully!")
