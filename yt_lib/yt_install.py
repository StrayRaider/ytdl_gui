from pytube import YouTube
from youtubesearchpython import VideosSearch
import os

directory = "../Musics/No-name"
history = True

search_url = ""
search_title = ""

def search(word, limit_arg=1):
    global search_url, search_title
    videosSearch = VideosSearch(word, limit = limit_arg)
    result = videosSearch.result()['result']
    #print(result)
    #print(result[0])
    video_1 = result[0]
    #print("\n",video_1['title'],"\n")
    
    #fotoğraf url
    #print(video_1['thumbnails'][0]['url'],"\n")
    search_title = video_1['title']
    search_url = video_1['link']
    #print(url)

search("eksik birşey mi var ali atay")

def search_get_info():
    global search_url, search_title
    return search_url, search_title

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
    global directory
    directory = dirct

def write_link(link,name):
    #list_file = open("links.txt","r")
    #lines = list_file.readlines()
    #for line in lines:
    #    print(line)
    #   #satıra '#' ile satıra yorum ekleme
    #list_file.close()
    w_list = []
    w_list.append("#"+ name +"\n")
    w_list.append(str(link)+"\n\n")
    list_file = open("links.txt","a")
    list_file.writelines(w_list)
    list_file.close()

def download(link):
    try:
        yt = YouTube(link)
    except:
        print(link,"linkde problem oluştu")
        exit()
    print("mp3_stream başladı")
    mp3 = yt.streams.filter(only_audio=True).first()
    print("mp3_stream bitti")
    out = mp3.download(directory)

    base, ext = os.path.splitext(out)
    name = base.split("/")[-1]
    print(name)
    to_mp3 = base + ".mp3"
    os.rename(out,to_mp3)
    if history:
        write_link(link,name)

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
