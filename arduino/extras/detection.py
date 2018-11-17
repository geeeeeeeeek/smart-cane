from imageai.Detection import ObjectDetection
import os
import time


# models could be found from
# https://github.com/OlafenwaMoses/ImageAI/tree/master/imageai/Detection
def detect(imagename, outputfile='detected.jpeg', model="resnet50_coco_best_v2.0.1.h5"):
    startTime = time.time()
    execution_path = os.getcwd()

    detector = ObjectDetection()
    if model == "yolo.h5":
        detector.setModelTypeAsYOLOv3()
    elif model == "yolo-tiny.h5":
        detector.setModelTypeAsTinyYOLOv3()
    else:
        detector.setModelTypeAsRetinaNet()

    detector.setModelPath(os.path.join(execution_path, model))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, imagename),
                                                 output_image_path=os.path.join(execution_path, outputfile))

    endTime = time.time()
    print("Model" + model)
    print("time of processing image: " + imagename)
    print(endTime - startTime)

    return detections


if __name__ == '__main__':
    image1 = "testImage1.png"
    image2 = "testImage2.png"
    model1 = "resnet50_coco_best_v2.0.1.h5"  # 150Mb
    model2 = "yolo.h5"  # 240Mb
    model3 = "yolo-tiny.h5"  # 35Mb

    testImage = "image2.jpg"

    detect(image1, "image1Detected_" + model1 + ".png", model1)
    detect(image2, "image2Detected_" + model1 + ".png", model1)
    # detect(testImage, "image2Detected_" + model1 + ".png", model1)

    detect(image1, "image1Detected_" + model2 + ".png", model2)
    detect(image2, "image2Detected_" + model2 + ".png", model2)
    # detect(testImage, "image2Detected_" + model2 + ".png", model2)

    detect(image2, "image2Detected_" + model3 + ".png", model3)
    detect(image1, "image1Detected_" + model3 + ".png", model3)
    # detect(testImage, "image1Detected_" + model3 + ".png", model3)
