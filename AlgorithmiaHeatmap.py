from flask import Flask, render_template, request

app = Flask(__name__)

import numpy as np
import Algorithmia
import cv2
import time

DEMO_IMG_PATH = 'static/demo_img.jpg'
OUT_IMG_PATH = 'static/demo_img_heatmap.jpg'


@app.route('/', methods=['GET', 'POST'])
def home_screen():
    if request.method == 'POST':

        # get form data
        multi = 'multi' in request.form
        alpha = float(request.form['overlay_alpha'])
        heatmap_class = request.form['heatmap_class']
        show_top_x_classes = int(request.form['show_top_x_classes'])

        start = time.time()
        avg_pred = generate_heatmap(multi, alpha, heatmap_class, show_top_x_classes)
        tot_time = '{:.2f}'.format(time.time() - start)

        return render_template('result.html', heatmap=OUT_IMG_PATH, avg_pred=avg_pred, tot_time=tot_time)

    else:
        return render_template('index.html', img=DEMO_IMG_PATH)


def generate_heatmap(multi, alpha, heatmap_class, show_top_x_classes):
    im = cv2.cvtColor(cv2.imread(DEMO_IMG_PATH), cv2.COLOR_BGR2RGB).tolist()

    api_configs = {
        'multi': multi,
        'image': im,
        'overlay_alpha': alpha,
        'heatmap_class': heatmap_class,
        'show_top_x_classes': show_top_x_classes
    }

    client = Algorithmia.client('simSF2RynCb7tuq3WjGq6EuxymG1')
    algo = client.algo('adsifubadsiufb/MyGithubHeatmapDemo/0.1.4')
    res = algo.pipe(api_configs).result

    heatmap = np.array(res['heatmap']).astype(np.uint8)
    avg_pred = res['avg_pred'].split('\n')

    cv2.imwrite(OUT_IMG_PATH, cv2.cvtColor(heatmap, cv2.COLOR_RGB2BGR))

    return avg_pred


if __name__ == '__main__':
    app.run()
