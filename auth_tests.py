from PIL import Image, ImageOps, ImageEnhance
from pytesseract import pytesseract
pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'
import cv2
def correct_image(
                  img: Image.Image,
                  threshold: int = 0,
                  threshold_max: int = -1,
                  invert: bool = True,
                  scale: float = 1,
                  contrast: float = 1,
                  brightness: float = 1,
                  ) -> Image.Image:
    tmp = img
    tmp = ImageOps.invert(tmp) if invert else tmp
    tmp = tmp.convert("L")
    tmp = (
        tmp.resize((round(tmp.width * scale), round(tmp.height * scale)))
        if scale != 1
        else tmp
    )
    tmp = ImageEnhance.Contrast(tmp).enhance(contrast) if contrast != 1 else tmp
    tmp = ImageEnhance.Brightness(tmp).enhance(brightness) if brightness != 1 else tmp
    if threshold == 0:
        pass
    elif threshold_max == -1:
        tmp = tmp.point(lambda x: 0 if x < threshold else x)
    else:
        tmp = tmp.point(lambda x: 0 if x < threshold else threshold_max)
    return tmp

def ocr_image( img: Image, whitelist: str = "0123456789,") -> str:
    print(fr'--oem 1 --psm 6 -c tessedit_char_whitelist={whitelist}')
    return pytesseract.image_to_string(img,config=fr'--oem 1 --psm 6 -c tessedit_char_whitelist=0123456789')

img = Image.open('resources/test_read.png')
# img_a = img.convert("RGB")
# img = correct_image(img)
# img = cv2.imread('resources\\test_read.png')
# print(ocr_image(img))

