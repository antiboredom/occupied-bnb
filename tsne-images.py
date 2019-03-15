import argparse
import sys
import numpy as np
import json
import os
from os.path import isfile, join
import keras
from keras.preprocessing import image
from keras.applications.imagenet_utils import decode_predictions, preprocess_input
from keras.models import Model
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from scipy.spatial import distance


def process_arguments(args):
    parser = argparse.ArgumentParser(description="tSNE on audio")
    parser.add_argument(
        "--images_path", action="store", help="path to directory of images"
    )
    parser.add_argument(
        "--output_path", action="store", help="path to where to put output json file"
    )
    parser.add_argument(
        "--num_dimensions",
        action="store",
        default=2,
        help="dimensionality of t-SNE points (default 2)",
    )
    parser.add_argument(
        "--perplexity",
        action="store",
        default=30,
        help="perplexity of t-SNE (default 30)",
    )
    parser.add_argument(
        "--learning_rate",
        action="store",
        default=150,
        help="learning rate of t-SNE (default 150)",
    )
    params = vars(parser.parse_args(args))
    return params


def get_image(path, input_shape):
    img = image.load_img(path, target_size=input_shape)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


def find_candidate_images(images_path):
    """
    Finds all candidate images in the given folder and its sub-folders.

    Returns:
        images: a list of absolute paths to the discovered images.
    """
    images = []
    for root, dirs, files in os.walk(images_path):
        for name in files:
            file_path = os.path.abspath(os.path.join(root, name))
            if (os.path.splitext(name)[1]).lower() in [".jpg", ".png", ".jpeg"]:
                images.append(file_path)
    return images


def analyze_images(images_path):
    # make feature_extractor
    model = keras.applications.VGG16(weights="imagenet", include_top=True)
    feat_extractor = Model(inputs=model.input, outputs=model.get_layer("fc2").output)
    input_shape = model.input_shape[1:3]
    # get images
    candidate_images = find_candidate_images(images_path)
    # analyze images and grab activations
    activations = []
    images = []
    for idx, image_path in enumerate(candidate_images):
        file_path = join(images_path, image_path)
        img = get_image(file_path, input_shape)
        if img is not None:
            print(
                "getting activations for %s %d/%d"
                % (image_path, idx, len(candidate_images))
            )
            acts = feat_extractor.predict(img)[0]
            activations.append(acts)
            images.append(image_path)
    # run PCA firt
    print("Running PCA on %d images..." % len(activations))
    features = np.array(activations)
    pca = PCA(n_components=300)
    pca.fit(features)
    pca_features = pca.transform(features)
    return images, pca_features


def run_tsne(
    images_path, output_path, tsne_dimensions, tsne_perplexity, tsne_learning_rate
):
    images, pca_features = analyze_images(images_path)
    print("Running t-SNE on %d images..." % len(images))
    X = np.array(pca_features)
    tsne = TSNE(
        n_components=tsne_dimensions,
        learning_rate=tsne_learning_rate,
        perplexity=tsne_perplexity,
        verbose=2,
    ).fit_transform(X)
    # save data to json
    data = []
    for i, f in enumerate(images):
        point = [
            float(
                (tsne[i, k] - np.min(tsne[:, k]))
                / (np.max(tsne[:, k]) - np.min(tsne[:, k]))
            )
            for k in range(tsne_dimensions)
        ]
        data.append(
            {"path": os.path.abspath(join(images_path, images[i])), "point": point}
        )
    with open(output_path, "w") as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    params = process_arguments(sys.argv[1:])
    images_path = params["images_path"]
    output_path = params["output_path"]
    tsne_dimensions = int(params["num_dimensions"])
    tsne_perplexity = int(params["perplexity"])
    tsne_learning_rate = int(params["learning_rate"])
    run_tsne(
        images_path, output_path, tsne_dimensions, tsne_perplexity, tsne_learning_rate
    )
    print("finished saving %s" % output_path)
