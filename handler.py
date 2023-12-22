import runpod
import os
import subprocess
import traceback
from tqdm import tqdm
import base64


def handler(event):
    print(event)


    images = event['input']['images']
    print(f"Images :- {images}")
    msg = ""
    failed_imgs = []
    if not isinstance(images, list):
        print(f"Expected list type for images but got {type(images)}")
        msg = f"Expected list type for images but got {type(images)}"
    if len(images) == 0:
        print(f"No image list passed")
        msg = "No images in list"
    else:
        images_folder = "./images"
        if not os.path.isdir(images_folder):
            os.mkdir(images)

        for ind, files in tqdm(enumerate(images)):
            try:
                with open(f"./{images_folder}/image-{ind}.jpg", "wb") as fh:
                    fh.write(base64.decodebytes(files))
                print(f"Successfully saved image :- image-{ind}.jpg in {images_folder}")
            except:
                print(f"Failed to save image :- image-{ind}.jpg")
                failed_imgs.append(f"image-{ind}.jpg")
                continue

            # Gen prompt for each image
            try:
                with open(f"./{images_folder}/image-{ind}.txt", 'w') as f:
                    f.write('a photo of [v] person')
                print(f"Successfully saved prompt :- image-{ind}.txt in {images_folder}")
            except:
                print(f"Failed to save prompt :- image-{ind}.txt")
                if os.path.isfile(f"{images_folder}/imag-{ind}.jpg"):
                    os.remove(f"{images_folder}/imag-{ind}.jpg")
        msg = "Preprocessed files"

        # train model
        cmd = "python3.10 training.py"
        try:
            res = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0:
                msg = f"Training completed"
                print(msg)
            else:
                msg = f"Training failed with:\n\nStdout:{res.stdout}\n\nStderr:{res.stderr}"
                print(msg)
        except subprocess.CalledProcessError as e:
            msg = f"Training failed with:\n\nException:{traceback.format_exc()}\n\nStdout:{e.stdout}\n\nStderr:{e.stderr}"
            print(msg)
        except: 
            msg = f"Training failed with:\n\nException:\n\n{traceback.format_exc()}"
            print(msg)
                

    return {"refresh_worker": True, "job_results": msg, "failed_images": failed_imgs}