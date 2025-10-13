import os
from PIL import Image
import base64

path = os.path.join('uploads', 'generated_by_model.png')
if not os.path.exists(path):
    print('MISSING')
else:
    img = Image.open(path)
    img.thumbnail((400, 400))
    import io
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode()
    print('data:image/png;base64,' + b64)
