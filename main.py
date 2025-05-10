import sys, os, os.path
import inspect

import importlib.util

import discord
from discord.commands import SlashCommand

from makefun import create_function

from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command
async def hi(context):
    await ctx.respond("This is how to do a normal slash command if anyone does fancy stuff.")

#dynamically import all the Python files we found.
def load_module(source, module_name):
    print(f"Loading module {module_name}")
    spec = importlib.util.spec_from_file_location(module_name, source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module

#Find all of the python files in the frogs folder
def find_files():
    return [f for f in os.listdir("frogs") if os.path.isfile(os.path.join("frogs", f)) and f.endswith(".py") and f != "main.py"]


#Iterate over our imported python files. Within each python file, look for methods that begin with "frog_"
#and register them as a slash command.
def register_frogs(files):
    for file in files:
        for frog in file.frogs:

            async def callback_impl(ctx, *args, **kwargs):
                await ctx.respond(frog["command"](ctx, *args, **kwargs))

            signature = inspect.signature(frog["command"])

            print(f"Signature: {signature}")
            print(f"Registering command {frog["command"]} from module {file} with name {frog["name"]}")

            #gets the signature that the user created and imposes that signature on top of our
            #impl func above to make a function with the right signature for discord to help with completions
            cmd = create_function(signature, callback_impl)

            bot.slash_command(name=frog["name"], description=frog["description"])(cmd)


def main():
    file_list = find_files()
    print(f"Found files {file_list}")
    loaded = [load_module(os.path.join("frogs", file), os.path.splitext(file)[0]) for file in file_list]
    frogs = register_frogs(loaded)

    bot.run(os.getenv('BOT_TOKEN'))


if __name__ == '__main__':
    main()

