import torch
from PIL.Image import Image
from diffusers import StableDiffusionXLPipeline
from pipelines.models import TextToImageRequest
from torch import Generator
from diffusers import AutoencoderKL


def load_pipeline() -> StableDiffusionXLPipeline:
    vae = AutoencoderKL.from_pretrained(
    'madebyollin/sdxl-vae-fp16-fix',
    use_safetensors=True,
    torch_dtype=torch.float16,
    ).to('cuda')
    pipeline = StableDiffusionXLPipeline.from_pretrained(
        "./models/newdream-sdxl-20",
        torch_dtype=torch.float16,
        local_files_only=True,
        vae=vae,
    ).to("cuda")

    pipeline(prompt="")

    return pipeline


def infer(request: TextToImageRequest, pipeline: StableDiffusionXLPipeline) -> Image:
    generator = Generator(pipeline.device).manual_seed(request.seed) if request.seed else None

    return pipeline(
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        width=request.width,
        height=request.height,
        generator=generator,
    ).images[0]
