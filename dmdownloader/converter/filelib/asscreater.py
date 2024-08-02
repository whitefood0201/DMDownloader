from dmdownloader.converter.asslib.dialogue import Dialogue
import dmdownloader.functional.FLfunctions as fl
import dmdownloader.functional.fileservice as fs


asscreater_template = "%(ifile)s --> %(ofile)s"
def create_file(global_config: dict, dialogues: list[Dialogue]) -> tuple[str, dict[str, str]]:
    '''
    Generate the ass file
    '''
    ofile = "{}{}.ass".format(global_config["ofile"], global_config["suffix"])
    head = get_header(global_config)
    text = "\n".join(fl.map(str, dialogues))

    fs.write_file(ofile, head+text)

    ''' return ofile name '''
    return ofile, {"ifile":global_config["ifile"], "ofile":ofile}

def get_header(global_config: dict) -> str:
    file = global_config["ass_head"]
    with open(file, "r", encoding="UTF-8") as file:
        template = file.read()
        x, y = global_config["resolution"].split("*")
        head = template.format(res_x=x, res_y=y, fontname=global_config["font_name"], fontsize=global_config["font_size"])
    return head + "\n"