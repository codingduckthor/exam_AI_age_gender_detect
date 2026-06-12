import cv2
import numpy as np
import base64

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

face_net = cv2.dnn.readNetFromCaffe(
    os.path.join(BASE_DIR, "models/face_detector/deploy.prototxt"),
    os.path.join(BASE_DIR, "models/face_detector/res10_300x300_ssd_iter_140000.caffemodel")
)

age_net = cv2.dnn.readNetFromCaffe(
    os.path.join(BASE_DIR, "models/age_detector/age_deploy.prototxt"),
    os.path.join(BASE_DIR, "models/age_detector/age_net.caffemodel")
)

gender_net = cv2.dnn.readNetFromCaffe(
    os.path.join(BASE_DIR, "models/gender_detector/gender_deploy.prototxt"),
    os.path.join(BASE_DIR, "models/gender_detector/gender_net.caffemodel")
)

AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)',
            '(25-32)', '(38-43)', '(48-53)', '(60-100)']

GENDER_LIST = ['Male', 'Female']

MODEL_MEAN_VALUES = (
    78.4263377603,
    87.7689143744,
    114.895847746
)


def predict(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    (h, w) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(
        image, 1.0, (300, 300), (104.0, 177.0, 123.0)
    )

    face_net.setInput(blob)
    detections = face_net.forward()

    results = []

    for i in range(detections.shape[2]):
        conf = detections[0, 0, i, 2]

        if conf > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")

            face = image[max(0,y1):max(0,y2), max(0,x1):max(0,x2)]

            if face.size == 0:
                continue

            face_blob = cv2.dnn.blobFromImage(
                face, 1.0, (227, 227),
                MODEL_MEAN_VALUES,
                swapRB=False
            )

            # AGE
            age_net.setInput(face_blob)
            age_preds = age_net.forward()
            age_idx = age_preds[0].argmax()

            # GENDER
            gender_net.setInput(face_blob)
            gender_preds = gender_net.forward()
            gender_idx = gender_preds[0].argmax()

            cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
            )

            label = f"{GENDER_LIST[gender_idx]}, {AGE_LIST[age_idx]}"

            cv2.putText(
                image,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            results.append({
                "age": AGE_LIST[age_idx],
                "age_confidence": float(age_preds[0][age_idx]),
                "gender": GENDER_LIST[gender_idx],
                "gender_confidence": float(gender_preds[0][gender_idx]),
                "box": [int(x1), int(y1), int(x2), int(y2)]
            })

    if len(results) == 0:
        return {
            "success": False,
            "message": "Лицо не найдено",
            "faces": []
        }

    _, buffer = cv2.imencode(".jpg", image)

    image_base64 = base64.b64encode(
        buffer
    ).decode("utf-8")

    return {
    "success": True,
    "faces": results,
    "image": image_base64
    }