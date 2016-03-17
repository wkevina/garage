import pygame.camera
import pygame.image
import PIL.Image

try:
    pygame.camera.init()
except ImportError:
    print('You are running on a platform that is not supported by '
              'pygame.camera')

video = None

def init():
    try:
        video = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    except:
        print('There is no camera device available')

def get_capture():
    if video:
        surf = video.get_image()
        return surface_to_image(surf)

def surface_to_image(surf):
    data = pygame.image.tostring(surf, "RGB")

    return PIL.Image.frombytes("RGB", surf.get_size(), data)
