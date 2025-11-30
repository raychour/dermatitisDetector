# All code below sourced from fastai course 2019

import uvicorn
import requests
from fastai.vision.all import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

# Compatibility shim for FastAI v1 models
import fastai.layers
import fastai.learner
import sys

if not hasattr(fastai.layers, 'FlattenedLoss'):
    class FlattenedLoss(CrossEntropyLossFlat): pass
    fastai.layers.FlattenedLoss = FlattenedLoss

if 'fastai.basic_train' not in sys.modules:
    sys.modules['fastai.basic_train'] = fastai.learner

export_file_url = 'https://www.dropbox.com/s/j8bvf35768lhpfk/export.pkl?dl=1'
export_file_name = 'export.pkl'

classes = ['eczema', 'measles', 'melanoma']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


import requests

def download_file(url, dest):
    if dest.exists(): return
    response = requests.get(url)
    response.raise_for_status()
    with open(dest, 'wb') as f:
        f.write(response.content)


def setup_learner():
    download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path / export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

learn = setup_learner()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = PILImage.create(BytesIO(img_bytes))
    prediction = learn.predict(img)[0]
    return JSONResponse({'result': str(prediction)})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
