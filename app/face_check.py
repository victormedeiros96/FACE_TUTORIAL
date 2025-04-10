# app/face_check.py
from pathlib import Path
from deepface import DeepFace
import glob

def check_person(input_image_path: str) -> str | None:
    def _check(img2):
        result = DeepFace.verify(img1_path=input_image_path, img2_path=img2, threshold=0.7,model_name='Facenet')
        result['path'] = img2
        return result

    results = list(map(_check, glob.glob('app/faces/*')))
    sorted_results = sorted(results, key=lambda r: abs(r.get('distance', float('inf'))))
    best_match = sorted_results[0]
    
    return Path(best_match.get('path')).stem if best_match.get('verified') else None
