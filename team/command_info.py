#by Hieu and Hai

class CommandInfo:
    def __init__(self, name, long_syntax, short_syntax, description, example):
        self.name = name
        self.long_syntax =long_syntax
        self.short_syntax = short_syntax
        self.description = description
        self.example = example
    def formatted_info (self):
        n = '*'+self.name+'*'
        ls = '    `'+self.long_syntax+'`'
        d = '    '+self.description
        e = "    Example: "+'`'+self.example+'`'
        s= ""
        for x in [n, ls, d, e]:
            s+= x
            s+= "\n"
        return s
# command register
rr_name = "Recipe recommendations"
rr_long_syntax = "/recipe ingredient1 ingredient2 ingredient3"
rr_short_syntax = "recipe"
rr_description = "Recommends recipes based on the ingredients inputed."
rr_example = "/recipe eggs bread butter"
cmd_recipe_rec = CommandInfo(rr_name, rr_long_syntax, rr_short_syntax, rr_description , rr_example )

#list of commands
commands = {
    cmd_recipe_rec.short_syntax : cmd_recipe_rec,
}
list_of_commands_name = commands.keys()