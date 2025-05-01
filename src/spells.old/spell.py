import lupa
import os

class Spell:
    def __init__(self, script_name: str, target):
        self.script_name = script_name

        self.lua = lupa.LuaRuntime()

        self.lua.execute(f"target = {}")

        print(self.lua.execute(open(script_name).read()))
    

spell = Spell(os.path.join('data', 'scripts', 'spell1.lua'))