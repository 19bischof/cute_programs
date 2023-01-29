import pathlib
import time
from PyPDF2 import PdfReader,PdfWriter
import os
from tkinter import filedialog
import getch
import shutil
from window_smart import win_focus
term_name = "PDF_curation😗"
if os.name == 'nt':
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW(term_name)
else:
    sys.stdout.write('\33]0;' + term_name + '\a')
    sys.stdout.flush()
my_win = win_focus(term_name)
temp_dir = f"delete_{time.time():.0f}"
try:
    os.mkdir(temp_dir)
except FileExistsError:
    pass
count = -1
new = {}
try:
    for file in filedialog.askopenfiles(filetypes=(("PDF's","*.pdf"),)):
        reader = PdfReader(file.name)
        for i,p in enumerate(reader.pages):
            count += 1
            with open(temp_dir+f"/temp_{count}.pdf","wb") as f:
                writer = PdfWriter()
                writer.add_page(p)
                writer.write(f)
            ind=None
            os.system('"'+pathlib.Path(f.name).absolute().as_posix()+'"')
            my_win.focus(delay=0.2)
            while inp:=getch.get_input(f"What Index should this page have?(number or 'none')").strip():
                if inp=="none":
                    break
                try:
                    ind = int(inp)
                    if ind in new:
                        ind=None
                        print("Index already taken. Try again")
                        continue
                except ValueError:
                    print("wasn't a number!")
                else:
                    new[ind] = p
                    break    
except KeyboardInterrupt:
    quit()
finally:
    shutil.rmtree(temp_dir)
    
publisher = PdfWriter()
for page in sorted(new):
    page = new[page]
    publisher.add_page(page)
with open(f"publish_{time.time():.0f}.pdf","wb") as f:
    publisher.write(f)
    print(f"Created PDF \"{f.name}\" with {len(publisher.pages)} pages")