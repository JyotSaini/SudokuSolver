from PIL import Image
from pathlib import Path
import os

currPath = Path(__file__).parent.absolute()

for root, directories, files in os.walk('test'):
    for filename in files:
        # Join the two strings in order to form the full filepath.
        filepath = os.path.join(root, filename)

        filepath = str(currPath) + "\\" + filepath.replace('/', '\\')

        if filepath.endswith('.jpg') or filepath.endswith('.jpeg') or filepath.endswith('.png'):
            img = Image.open(filepath).convert('L')
            img.save(filepath)