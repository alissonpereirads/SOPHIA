from PIL import Image
import re
import plotly.graph_objects as go


def load_images(icon1_path, icon2_path):
    icon1 = Image.open(icon1_path)
    icon2 = Image.open(icon2_path)
    return icon1, icon2
