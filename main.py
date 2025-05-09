import sys, os, os.path
import inspect

import importlib.util

import discord
from discord.commands import SlashCommand

from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

#dynamically import all the Python files we found.
def load_module(source, module_name):
    print(f"Loading module {module_name}")
    spec = importlib.util.spec_from_file_location(module_name, source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module

#Find all of the python files in the frogs folder
def find_extensions():
    return [f for f in os.listdir("frogs") if os.path.isfile(os.path.join("frogs", f)) and f.endswith(".py") and f != "main.py"]

#Iterate over our imported python files. Within each python file, look for methods that begin with "frog_"
#and register them as a slash command.
def register_frogs(exts):

    frogs = []
    for ext in exts:
        frogs = [f for f in dir(ext) if f.startswith("frog_")]
        for name in frogs:
            frog = getattr(ext, name)

            spec = inspect.getfullargspec(frog)
            #This is to figure out the name of the function using the name kwarg.
            #It feels like a dirty hack, probably because it is. But as long as there's only one default argument
            #it works without adding any extra stuff into our user code.
            name = spec.defaults[0]

            print(f"Registering method {frog} from module {ext} with name {name}")

            async def callback_stub(ctx):
                await ctx.respond(frog(ctx))

            bot.slash_command(name=name)(callback_stub)


def main():
    ext_list = find_extensions()
    print(f"Found extensions {ext_list}")
    exts = [load_module(os.path.join("frogs", ext), os.path.splitext(ext)[0]) for ext in ext_list]
    frogs = register_frogs(exts)

    bot.run(os.getenv('BOT_TOKEN'))


if __name__ == '__main__':
    main()

