import os
import cv2
import dlib
import numpy as np

# Define rutas dinámicas basadas en el archivo actual
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "../models")
PREDICTOR_PATH = os.path.join(MODELS_DIR, "shape_predictor_68_face_landmarks.dat")
FACE_REC_MODEL_PATH = os.path.join(MODELS_DIR, "dlib_face_recognition_resnet_model_v1.dat")

# Verifica que los modelos existen antes de cargarlos
if not os.path.exists(PREDICTOR_PATH):
    raise FileNotFoundError(f"El archivo de predicción no se encontró: {PREDICTOR_PATH}")
if not os.path.exists(FACE_REC_MODEL_PATH):
    raise FileNotFoundError(f"El modelo de reconocimiento facial no se encontró: {FACE_REC_MODEL_PATH}")

def preprocess_face(image, detector, shape_predictor, target_size=(150, 150)):
    """Recorta y normaliza el rostro detectado."""
    faces = detector(image)
    if len(faces) == 0:
        return None  # No se detectó ningún rostro
    face = faces[0]  # Tomar el primer rostro detectado
    shape = shape_predictor(image, face)
    aligned_face = dlib.get_face_chip(image, shape, size=target_size[0])
    return aligned_face

def compare_faces(dni_photo_path: str, webcam_photo_path: str) -> bool:
    # Cargar imágenes
    dni_image = cv2.imread(dni_photo_path)
    webcam_image = cv2.imread(webcam_photo_path)

    if dni_image is None or webcam_image is None:
        print("Error al cargar una o ambas imágenes. Verifica las rutas.")
        return False

    # Convertir imágenes a RGB
    dni_image = cv2.cvtColor(dni_image, cv2.COLOR_BGR2RGB)
    webcam_image = cv2.cvtColor(webcam_image, cv2.COLOR_BGR2RGB)

    # Configurar modelos de Dlib
    detector = dlib.get_frontal_face_detector()
    shape_predictor = dlib.shape_predictor(PREDICTOR_PATH)
    face_rec_model = dlib.face_recognition_model_v1(FACE_REC_MODEL_PATH)

    # Preprocesar rostros
    dni_face = preprocess_face(dni_image, detector, shape_predictor)
    webcam_face = preprocess_face(webcam_image, detector, shape_predictor)

    if dni_face is None or webcam_face is None:
        print("No se pudo detectar un rostro en una de las imágenes.")
        return False

    # Obtener descriptores de rostro
    dni_descriptor = face_rec_model.compute_face_descriptor(dni_face)
    webcam_descriptor = face_rec_model.compute_face_descriptor(webcam_face)

    # Comparar descriptores usando distancia euclidiana
    distance = np.linalg.norm(np.array(dni_descriptor) - np.array(webcam_descriptor))
    print(f"Distancia entre descriptores: {distance}")

    # Umbral ajustado para rostros similares
    threshold = 0.6  # Ajusta según tus necesidades
    if distance < threshold:
        print("Los rostros son iguales.")
        return True
    else:
        print("Los rostros no son iguales.")
        return False
