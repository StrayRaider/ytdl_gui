from pytube import YouTube
from pytube import Playlist
from youtubesearchpython import VideosSearch
import os

directory = "../Musics/No-name"
history = True
is_loop_running = False
song_list = []

def search(word, limit_arg=1):
    global song_list
    song_list.clear()
    videosSearch = VideosSearch(word, limit = limit_arg)
    result_list = videosSearch.result()['result']
    #print(result,"\n")
    #print(result[0],"\n")
    #print(result[1],"\n")
    #video_1 = result[0]
    #print("\n",video_1['title'],"\n")
    
    #fotoğraf url
    #print(video_1['thumbnails'][0]['url'],"\n")
    for result in result_list:
        song = [result['title'],result['link']]
        song_list.append(song)

#search("eksik birşey mi var ali atay")

def search_get_info():
    global song_list
    return song_list

def loop(link_list,parent,installation_type):
    global directory
    parent.spinner.start()
    is_loop_running = True
    print("loop başladı")
    install_count = 0
    line_c = 1
    installed = 0
    for link in link_list:
        print("döngü")
        if link != "":
            if link[0] != "#":
                if link[0] == "/":
                    install_count += 1
                else:
                    if link[0] == "*":
                        directory = link[1::]
                    else:
                        if install_count == 1 or True:
                            #oynatma listesi
                            installed += 1
                            print("download",line_c)
                            download_link(link,installation_type)
                            parent.progressbar.set_fraction(parent.progressbar.get_fraction()+1/len(link_list))
            else:
                print(link)
        line_c +=1
    parent.loop_stoped()
    is_loop_running = False

    print("done")
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

def download_playlist(playlist_link,download_type):
    playL = Playlist(playlist_link)
    for video in playL: 
        if download_type == "mp3":
            download_mp4(video)
        else:
            download_mp3(video)

def download_mp4(yt,res="720p"):
    mp4 = yt.streams.filter(res,mime_type="video/mp4").first()
    out = mp4.download(directory)
    print("mp4_stream bitti")


def download_mp3(yt):
    mp3 = yt.streams.filter(only_audio=True).first()
    out = mp3.download(directory)
    print("mp3_stream bitti")
    base, ext = os.path.splitext(out)
    name = base.split("/")[-1]
    print(name)
    to_mp3 = base + ".mp3"
    os.rename(out,to_mp3)
    if history:
        write_link(link,name)

def download_link(link,download_type):
    try:
        yt = YouTube(link)
    except:
        print(link,"linkde problem oluştu")
        return None
        #exit()
    print("mp3_stream başladı")
    if download_type == "mp3":
        download_mp3(yt)
    else:
        download_mp4(yt)

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
