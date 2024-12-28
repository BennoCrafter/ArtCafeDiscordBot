import os
import random
import interactions
from src import logutil
from pathlib import Path
import json


logger = logutil.init_logger(os.path.basename(__file__))
prompts_path = Path("resources/art_prompts.json")

class Prompt:
    def __init__(self, prompt: str, author: str, id: int):
        self.prompt = prompt
        self.author = author
        self.id = id

    def __str__(self):
        return f"{self.prompt}||{self.author}"

    def to_dict(self):
        return {"prompt": self.prompt, "author": self.author, "id": self.id}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["prompt"], data["author"], data["id"])

def read_prompts() -> list[Prompt]:
    """
    Example:
        "My Prompt", "Bot Generated"
        "Second Prompt", "Bot Generated"
    """
    prompts: list[Prompt] = []
    prompt_data = json.load(prompts_path.open())
    for prompt in prompt_data:
        prompts.append(Prompt.from_dict(prompt))
    return prompts

def write_prompts(prompts: list[Prompt]):
    prompt_data = []
    for prompt in prompts:
        prompt_data.append(prompt.to_dict())
    json.dump(prompt_data, prompts_path.open(mode="w"), indent=4)


class PromptCog(interactions.Extension):
    art_prompts: list[Prompt] = read_prompts()

    @interactions.slash_command(
        "prompt", description="Get an art prompt"
    )
    @interactions.slash_option("prompt_id", "The index of the prompt to get", required=False, opt_type=interactions.OptionType.INTEGER)
    async def prompt(self, ctx: interactions.SlashContext, prompt_id: int | None = None):
        art_prompt = random.choice(self.art_prompts) if prompt_id is None else self.get_prompt_by_id(prompt_id)
        if not art_prompt:
            await ctx.send("Prompt not found!", ephemeral=True)
            return

        e = interactions.Embed(title="Art Prompt", description=art_prompt.prompt, color=interactions.Color.random())
        e.set_footer(text=f"By: {art_prompt.author} | Nr: {art_prompt.id}")
        await ctx.send(embed=e)


    @interactions.slash_command(
        "remove_prompt", description="Delete an art prompt by id"
    )
    @interactions.slash_option("prompt_id", "The index of the prompt to delete", required=True, opt_type=interactions.OptionType.INTEGER)
    async def remove_prompt(self, ctx: interactions.SlashContext, prompt_id: int):
        try:
            if 0 <= prompt_id < len(self.art_prompts):
                to_remove_prompt = self.get_prompt_by_id(prompt_id)
                if not to_remove_prompt:
                    await ctx.send(f"Could not find prompt with ID {prompt_id}", ephemeral=True)
                    return

                self.art_prompts.remove(to_remove_prompt)
                write_prompts(self.art_prompts)

                e = interactions.Embed(title="Prompt Removed", description=f"Removed prompt: {to_remove_prompt.prompt}", color=interactions.Color.random())
                e.set_footer(text=f"Originally by: {to_remove_prompt.author}")
                await ctx.send(embed=e)
            else:
                await ctx.send("Invalid prompt ID - must be between 0 and " + str(len(self.art_prompts)-1), ephemeral=True)
        except Exception as err:
            logger.error(f"Error removing prompt: {err}")
            await ctx.send("Failed to remove prompt!", ephemeral=True)

    @interactions.slash_command(
        "add_prompt", description="Add an art prompt"
    )
    @interactions.slash_option("prompt", "The prompt to add", required=True, opt_type=interactions.OptionType.STRING)
    async def add_prompt(self, ctx: interactions.SlashContext, prompt: str):
        try:
            author: str = ctx.author.display_name
            prompt_id = len(self.art_prompts)
            self.art_prompts.append(Prompt(prompt, author, prompt_id))
            write_prompts(self.art_prompts)
            e = interactions.Embed(title="Prompt Added", description=f"Added prompt: {prompt}", color=interactions.Color.random())
            e.set_footer(text=f"By: {author}")
            await ctx.send(embed=e)
        except Exception as err:
            logger.error(f"Error adding prompt: {err}")
            await ctx.send("Failed to add prompt!", ephemeral=True)

    def get_prompt_by_id(self, prompt_id: int) -> Prompt | None:
        for prompt in self.art_prompts:
            if prompt.id == prompt_id:
                return prompt
        return None
