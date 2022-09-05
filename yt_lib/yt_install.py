from pytube import YouTube
import os

directory = "../Music/No-name"

def loop(link_list):
    global directory
    install_count = 0
    line_c = 1
    installed = 0
    for link in link_list:
        if link != "":
            if link[0] != "#":
                if link[0] == "/":
                    install_count += 1
                else:
                    if link[0] == "*":
                        directory = link[1::]
                    else:
                        if install_count == 1:
                            #oynatma listesi
                            installed += 1
                            print("download",line_c)
                            download(link)
            else:
                print(link)
        line_c +=1
    return installed

def set_dir(dirct):
    directory = dirct

def download(link):
    try:
        yt = YouTube(link)
    except:
        print(link,"linkde problem oluştu")
        exit()
    mp3 = yt.streams.filter(only_audio=True).first()
    out = mp3.download(directory)

    base, ext = os.path.splitext(out)
    to_mp3 = base + ".mp3"
    os.rename(out,to_mp3)

def list_obj():
    dosyalar = os.listdir(directory)
    print(dosyalar)

def set_link_list():
    #os ile dosyadan linkleri çekme
    #ve faha önce indirilmiş olan linkleri çıkartma
    try:
        f = open("links.txt","r")
        link_list = f.read().split("\n")
        del link_list[-1]
        f.close()
        return link_list
    except:
        return None

#link_list = set_link_list()
#line = loop(link_list)

#print("installation compleated.",line," sound downloaded")
