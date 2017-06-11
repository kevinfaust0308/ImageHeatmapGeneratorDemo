from flask import Flask, render_template, request

app = Flask(__name__)

import numpy as np
import Algorithmia
import matplotlib.pyplot as plt
import time


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
        tot_time = time.time() - start
        heatmap = 'static/heatmap.jpg'

        return render_template('result.html', heatmap=heatmap, avg_pred=avg_pred, tot_time=tot_time)

    else:
        img = 'static/demo_img.jpg'
        return render_template('index.html', img=img)


def generate_heatmap(multi, alpha, heatmap_class, show_top_x_classes):
    im = plt.imread('static/demo_img.jpg').tolist()

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

    plt.imsave('static/heatmap.jpg', heatmap)

    return avg_pred


if __name__ == '__main__':
    app.run()
