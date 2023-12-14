import torch
from PIL import Image
from io import BytesIO

from diffusers import StableDiffusionImg2ImgPipeline

def run(input_image, prompt):
    import os
    # Use Apple Metal Performance Shaders on Mac
    device = "mps"
    model_id_or_path = os.path.join(os.path.dirname(__file__), "checkpoint", "v2-1_768-ema-pruned.ckpt")
    pipeline = StableDiffusionImg2ImgPipeline.from_single_file(model_id_or_path, torch_dtype=torch.float16)
    pipeline = pipeline.to(device)
    # Recommended if your computer has < 64 GB of RAM
    pipeline.enable_attention_slicing()

    init_image = Image.open(input_image).convert("RGB")
    init_image = init_image.resize((768, 512))

    images = pipeline(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images
#    images[0].save("fantasy_landscape.png")
    return images

def fetch_image(url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"):
    import requests
    response = requests.get(url)
    return BytesIO(response.content)