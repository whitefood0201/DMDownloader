import os as os

class AssCreater:
    
    def __init__(self, config, dialogues):
        self.config = config

        self.ofile = self.ofilename(config["ofile"])

        self.dialogues = dialogues

    def ofilename(self, name: str) -> str:
        return "{}{}.ass".format(name, self.config["suffix"])

    def create_file(self) -> str:
        ''' return ofile name '''
        head = self.get_header()
        text = "\n".join([str(dialogue) for dialogue in self.dialogues])

        if not os.path.exists("./downloads/"): os.mkdir("./downloads/")            
        with open(self.ofile, "w", encoding="UTF-8") as file:
            file.write(head)
            file.write(text)
            file.flush()

        return self.ofile

    def get_header(self):
        file = self.config["ass_head"]
        with open(file, "r", encoding="UTF-8") as file:
            template = file.read()
            x, y = self.config["resolution"].split("*")
            head = template.format(res_x=x, res_y=y, fontname=self.config["font_name"], fontsize=self.config["font_size"])

        return head + "\n"
    
