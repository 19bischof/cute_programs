import ftplib, os
import settings as st
import datetime
ftp = ftplib.FTP(st.ip,st.user,st.passwd)

def get_file(file_name = st.file_name):
    with open(file_name,'wb') as f:
        try:
            ftp.retrbinary('RETR %s' % st.file_path, f.write)
        except ftplib.error_perm:
            pass
        
def append_to_file(url):
    with open(st.file_name, 'rb') as f:
        try:  # catch OSError in case of a one line file 
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
    if last_line and last_line.split()[1] == url:
        return
    date = datetime.datetime.now().isoformat()
    with open(st.file_name,'a') as f:
        f.write('\n'+date + ' ' + url)
        
def upload_new_file() :
    tmp_file = 'verify_history.txt'
    get_file(tmp_file)
    if os.stat(tmp_file).st_size > os.stat(st.file_name).st_size:
        return
    with open(st.file_name,'rb') as f:
        ftp.storbinary('STOR ' + st.file_path, f) 
