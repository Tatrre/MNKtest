import ftplib 

def connect():
    ftp = ftplib.FTP('138.201.56.185')
    ftp.login(user='rekrut', passwd='zI4wG9yM5krQ3d')
    return ftp

def list():
    ftp = connect()
    print(ftp.nlst())
    ftp.quit() 


def download(filename):
    ftp = connect()
    with open('files/task.rar', 'wb') as f : 
        ftp.retrbinary("RETR " + filename, f.write)

    ftp.quit()

def upload(local_file):
    ftp = connect()
    with open(local_file, 'rb') as f:
        ftp.storbinary('STOR '+ '/complete/Tatre/' + 'export.csv' , f)
    ftp.quit()        
