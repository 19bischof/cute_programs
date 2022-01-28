import pathlib
from time import sleep
def dir_parse(p:pathlib.Path,depth):
    # input(p)

    for new in p.glob("*"):
        print("    "*depth,end="")
        if depth != 0:
            print("|___ ",end="")
        print(new.name)
        if new.is_dir():
            dir_parse(new,depth+1)

root = pathlib.Path("./").absolute()
grandgrandpa_of_root = root.parent.parent.parent

print(grandgrandpa_of_root.absolute())
print(grandgrandpa_of_root.as_uri())
sleep(2)
dir_parse(grandgrandpa_of_root,0)