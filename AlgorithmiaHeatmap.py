from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import time
import os

from heatmap_api import generate_heatmaps_and_preds, upload_files_to_api

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'


@app.route('/', methods=['GET', 'POST'])
def home_screen():
    if request.method == 'POST':

        # get form data
        multi = 'multi' in request.form
        alpha = float(request.form['overlay_alpha'])
        heatmap_class = request.form['heatmap_class']
        show_top_x_classes = int(request.form['show_top_x_classes'])

        # get all selected files
        selected_file_paths = request.files.getlist("multiplefiles")

        uploaded_flask_files = []
        for f in selected_file_paths:
            # upload
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filename = 'uploads/' + filename
            uploaded_flask_files.append(filename)

        # upload the images uploaded to flask to our api which will temporary store the images for 24 hours
        api_file_paths = upload_files_to_api(uploaded_flask_files)

        start = time.time()
        # generate heatmaps and predictions
        static_heatmap_paths, avg_preds = generate_heatmaps_and_preds(api_file_paths, multi, alpha, heatmap_class,
                                                                      show_top_x_classes)
        tot_time = '{:.2f}'.format(time.time() - start)

        # selected_file_paths to display image title and static_heatmap_paths for loading image/download
        data = zip(selected_file_paths, static_heatmap_paths, avg_preds)

        return render_template('result.html', data=data, tot_time=tot_time)

    else:
        # heatmaps = ['static/demo_img_heatmap.jpg', 'static/demo_img_heatmap.jpg', 'static/demo_img_heatmap.jpg']
        # avg_preds = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        # files = ['jaja.jpy', 'adfdf', 'adsfsdf']
        # data = zip(files, heatmaps, avg_preds)
        #
        # return render_template('result.html', data=data, tot_time='53.43')

        return render_template('index.html')


if __name__ == '__main__':
    app.run()
