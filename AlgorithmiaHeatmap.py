from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

import time
import os

from heatmap_api import generate_heatmaps_and_preds, upload_files_to_api

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(os.path.dirname(app.config['UPLOAD_FOLDER']), exist_ok=True)  # create uploads directory if not exist yet


@app.route('/', methods=['GET', 'POST'])
def home_screen():
    if request.method == 'POST':

        # import sys
        #
        # print('file name of uploaded: ' + str(request.files.getlist("upload_img")[0].filename), file=sys.stderr)
        # print('file uploaded: ' + str(request.files.getlist("upload_img")[0]), file=sys.stderr)
        #
        # print('file name of demo: ' + str(request.form.getlist("demo_img")), file=sys.stderr)
        # #print('file name of demo: ' + str(request.form.getlist("demo_img")[0]), file=sys.stderr)
        #
        # return 'ja'


        # get form data
        multi = 'multi' in request.form
        alpha = float(request.form['overlay_alpha'])
        heatmap_class = request.form['heatmap_class']
        show_top_x_classes = int(request.form['show_top_x_classes'])

        # to hold all the uploaded image paths on our flask server which we will upload to our api
        uploaded_flask_files = []
        # names of all selected files to show on results screen
        selected_file_names = []

        # check if any files were uploaded
        # even if nothing was sent, we will still have 1 file object with a empty file name
        if request.files.getlist("upload_img")[0].filename:

            # add all the file names to our list
            selected_file_names += [fileobj.filename for fileobj in request.files.getlist("upload_img")]

            # upload each locally selected file to our server
            for file_obj in request.files.getlist("upload_img"):
                # upload
                filename = secure_filename(file_obj.filename)
                file_obj.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filename = app.config['UPLOAD_FOLDER'] + filename
                uploaded_flask_files.append(filename)

        selected_file_names += ["(DEMO) " + name for name in request.form.getlist("demo_img")]
        uploaded_flask_files += ["static/" + name for name in request.form.getlist('demo_img')]

        # TODO: currently assuming at least 1 image is selected/uploaded

        # upload the images uploaded to flask to our api which will temporary store the images for 24 hours
        api_file_paths = upload_files_to_api(uploaded_flask_files)

        start = time.time()
        # generate heatmaps and predictions
        static_heatmap_paths, avg_preds = generate_heatmaps_and_preds(api_file_paths, multi, alpha, heatmap_class,
                                                                      show_top_x_classes)
        tot_time = '{:.2f}'.format(time.time() - start)

        # selected_file_paths to display image title and static_heatmap_paths for loading image/download
        data = zip(selected_file_names, static_heatmap_paths, avg_preds)

        return render_template('result.html', data=data, tot_time=tot_time)

    else:
        # heatmaps = ['static/Lesion1.jpg', 'static/Lesion1.jpg', 'static/Lesion1.jpg']
        # avg_preds = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        # files = ['jaja.jpy', 'adfdf', 'adsfsdf']
        # data = zip(files, heatmaps, avg_preds)
        #
        # return render_template('result.html', data=data, tot_time='53.43')

        return render_template('index.html')


if __name__ == '__main__':
    app.run()
