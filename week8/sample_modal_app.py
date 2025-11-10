import io
import os

import modal


app = modal.App()

"""A Modal app that runs Stable Diffusion to generate images from text prompts."""
@app.function(
    image=modal.Image.debian_slim().pip_install("torch", "diffusers[torch]", "transformers", "ftfy"),
    secrets=[modal.Secret.from_name("hf-secret")],
    gpu="any",
)

# Define the function that runs Stable Diffusion
def run_stable_diffusion(prompt: str):
    from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion import StableDiffusionPipeline

    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        use_auth_token=os.environ["HF_TOKEN"],
    ).to("cuda")

    
    result = pipe(prompt, num_inference_steps=10)
    # result can be a PipelineOutput with .images or a tuple; handle both cases
    if isinstance(result, tuple):
        image = result[0]
    elif hasattr(result, "images"):
        image = result.images[0]
    else:
        raise ValueError("Unexpected result type from StableDiffusionPipeline")

    from PIL import Image
    import numpy as np
    import torch

    buf = io.BytesIO()
    # Convert image to PIL Image if needed
    if isinstance(image, torch.Tensor):
        image = image.detach().cpu().numpy()
    if isinstance(image, np.ndarray):
        # If image is (C, H, W), transpose to (H, W, C)
        if image.ndim == 3 and image.shape[0] in [1, 3, 4]:
            image = np.transpose(image, (1, 2, 0))
        image = Image.fromarray((image * 255).astype(np.uint8))
    image.save(buf, format="PNG")
    img_bytes = buf.getvalue()

    return img_bytes


# Define a local entrypoint to run the function
@app.local_entrypoint()
def main():
    img_bytes = run_stable_diffusion.remote("Wu-Tang Clan climbing Mount Everest")
    with open("/images/output.png", "wb") as f:
        f.write(img_bytes)


# where should I see the generated image?
    print("Image saved to /images/output.png")
    return img_bytes
