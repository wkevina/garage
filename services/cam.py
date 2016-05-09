import pygame.camera
import pygame.image
import PIL.Image

try:
    pygame.camera.init()
except ImportError:
    print('You are running on a platform that is not supported by '
              'pygame.camera')
    raise

video = None

def init(device=None):
    try:
        if device:
            video = pygame.camera.Camera(device)
        else:
            video = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    except:
        print('There is no camera device available')
        raise

def capture():
    """
    Capture a frame from the video camera and return it as a PIL.Image.Image
    """
    surf = video.get_image()

    return surface_to_image(surf)

def surface_to_image(surf):
    data = pygame.image.tostring(surf, "RGB")

    return PIL.Image.frombytes("RGB", surf.get_size(), data)
