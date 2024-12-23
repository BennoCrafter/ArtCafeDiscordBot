# Art Café Discord Bot

This is a Discord bot for the Art Café Discord server. It is written in python and uses the `discord-py-interactions` library.

## Features

### Admin Commands

- `/clear <amount>`: Clears the specified amount of messages in the channel.
- `/ticket setup`: Sets up a ticket system in the channel.

### Art Café Commands

#### Prompt Commands

- `/prompt`: Sends a random prompt to draw.
- `/prompt <promptid>`: Sends a specific prompt by its id to draw.
- `/add_prompt <prompt>`: Adds a prompt to the list of prompts.
- `/remove_prompt <promptid>`: Removes a prompt from the list of prompts.

#### Event Commands

- `/event create <name> <description> <end_date>`: Creates an event with the specified name, description and end date.
- `/event close` : Closes the current event.
- `/event results`: Shows the results of the current event.
- `/submit <attachment>`: Submits an entry to the current event.

#### Roleplay Commands

- `/roleplay bonk <@user>`: Bonk someone
- `/roleplay cuddle <@user>`: Cuddle someone
- `/roleplay highfive <@user>`: High five someone
- `/roleplay hug <@user>`: Hug someone
- `/roleplay kiss <@user>`: Kiss someone
- `/roleplay pat <@user>`: Pat someone
- `/roleplay poke <@user>`: Poke someone
- `/roleplay slap <@user>`: Slap someone
- `/roleplay wave <@user>`: Wave at someone
