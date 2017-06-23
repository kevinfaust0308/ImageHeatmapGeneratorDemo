import Algorithmia
import uuid
import os
import shutil

# api configurations
API_KEY = 'simSF2RynCb7tuq3WjGq6EuxymG1'
ALGORITHM = 'adsifubadsiufb/MyGithubHeatmapDemo/0.1.8'
client = Algorithmia.client(API_KEY)

# file io
TEMP_API_IMG_PATH = "data://.algo/adsifubadsiufb/MyGithubHeatmapDemo/temp"
HEATMAP_OUTPUT_PATH = os.path.join("static", "heatmaps")

os.makedirs(HEATMAP_OUTPUT_PATH, exist_ok=True)  # create heatmaps directory if not exist yet


def upload_files_to_api(file_paths):
    '''
    Uploads all uploaded flask files to the api server

    :param file_paths: file paths of images uploaded to flask
    :return: file paths of images on the api server
    '''

    # paths to image locations on api data server
    temp_image_paths = []

    for fp in file_paths:
        temp_img_path = "{}/{}.jpg".format(TEMP_API_IMG_PATH, str(uuid.uuid4()))

        # upload image to private temporary data hosting
        client.file(temp_img_path).putFile(fp)

        temp_image_paths.append(temp_img_path)

    return temp_image_paths


def generate_heatmaps_and_preds(file_paths, multi, alpha, heatmap_class, show_top_x_classes):
    '''
    Generates heatmap and total prediction for the given files

    :param file_path: location of uploaded image to generate heatmap on
    :return: file path to heatmap within static folder, average prediction
    '''

    api_configs = {
        'multi': multi,
        'overlay_alpha': alpha,
        'heatmap_class': heatmap_class,
        'show_top_x_classes': show_top_x_classes
    }
    # connect to api and dont time out for up to 50 minutes (max time)
    algo = client.algo(ALGORITHM).set_options(timeout=3000)

    # generated heatmaps and preds
    static_heatmap_paths = []
    avg_preds = []

    for fp in file_paths:
        # add image path to api config
        api_configs['image_path'] = fp

        res = algo.pipe(api_configs).result

        # api returns 2 things for now
        avg_pred = res['avg_pred']
        api_heatmap_path = res['heatmap_path']

        # download heatmap file into a temp folder
        temp_downloaded_heatmap_path = client.file(api_heatmap_path).getFile().name
        # move from temp folder to our static folder for html display
        temp_file_name = os.path.basename(temp_downloaded_heatmap_path)
        static_heatmap_path = os.path.join(HEATMAP_OUTPUT_PATH, "{}.jpg".format(temp_file_name))
        os.rename(temp_downloaded_heatmap_path, static_heatmap_path)

        # add our generated result to our list
        static_heatmap_paths.append(static_heatmap_path)
        avg_preds.append(avg_pred)

    return static_heatmap_paths, avg_preds
