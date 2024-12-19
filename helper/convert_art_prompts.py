from pathlib import Path
import json

def convert_art_prompts(prompts_path: Path, output_path: Path):
    with open(prompts_path, "r") as f:
        prompts = f.read().splitlines()
    prompts = [prompt.split("||") for prompt in prompts]

    output = []
    for i, prompt in enumerate(prompts):
        output.append({"prompt": prompt[0], "author": prompt[1], "id": i})
    json.dump(output, open(output_path, "w"), indent=4)

if __name__ == "__main__":
    convert_art_prompts(Path("resources/art_prompts.txt"), Path("resources/art_prompts.json"))
