import os
import sys

import pystray
from PIL import Image, ImageDraw
from loguru import logger
from pystray import MenuItem

from src.const import const


def create_image():
    width = 64
    height = 64
    color1 = 'black'
    color2 = 'red'
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2,
    )
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2,
    )
    return image


def exit_action(icon, item):
    icon.stop()
    logger.info('Exiting tray')
    sys.exit(0)


def setup_tray():
    if os.path.exists('app_icon.ico'):
        icon_image = Image.open('app_icon.ico')
    else:
        icon_image = create_image()
    icon = pystray.Icon(
        'WT Discord RPC',
        icon_image,
        'WT Discord RPC',
        menu=pystray.Menu(
            MenuItem(const.presence_lang.close_tray['en'], exit_action)
        )
    )
    icon.run()
