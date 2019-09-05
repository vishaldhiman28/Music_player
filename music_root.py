import sys
from PyQt5.QtWidgets import QWidget,QApplication,QMainWindow,QPushButton,QAction,QMessageBox,QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot,QUrl
from PyQt5.QtMultimedia import QMediaPlaylist,QMediaPlayer,QMediaContent
import eyed3 
from eyed3 import *

class Music_App(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.title='Music Player'
        self.left=20
        self.top=30
        self.width=600
        self.height=400
        self.root_Gui()
        self.song_path=""
        self.q_path=""
        #initializing playlist and player

        self.Playlist=QMediaPlaylist()
        self.Player=QMediaPlayer()
        
        self.button_stat = -1
        #self.sp_st_cam= -1
        
      

    def root_Gui(self):
        #base of GUI

        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.menu()
        self.main_buttons()
        self.status_bar()
        self.show()
    

    def menu(self):
        #menu of GUI 
        
        main_menu=self.menuBar()
        file_menu=main_menu.addMenu('File')
        tools_menu=main_menu.addMenu('Tools')
        help__menu=main_menu.addMenu('Help')
        exit_=main_menu.addMenu('Exit')

        
        file_menu.addAction(self.open_file())
        file_menu.addAction(self.exit_button())
        exit_.addAction(self.exit_button()) 

    def main_buttons(self):
        #different button available in GUI

        play_button=QPushButton('Play',self)
        play_button.setToolTip("To play the song click it.")
        play_button.move(100,80)
        play_button.clicked.connect(self.play_button)
        
        pause_button=QPushButton('Pause',self)
        pause_button.setToolTip("To pause the song click it.")
        pause_button.move(200,80)
        pause_button.clicked.connect(self.pause_button)

        next_button=QPushButton('Next',self)
        next_button.setToolTip('Play Next Song')
        next_button.move(300,80)
        next_button.clicked.connect(self.next_button)

        prev_button=QPushButton('Prev',self)
        prev_button.setToolTip('Play Previous Song')
        prev_button.move(400,80)
        prev_button.clicked.connect(self.prev_button)

         
        plusV_button=QPushButton('+ Vol',self)
        plusV_button.setToolTip('Increase Volume')
        plusV_button.move(100,110)
        plusV_button.clicked.connect(self.plusV_button)

        minsV_button=QPushButton('- Vol',self)
        minsV_button.setToolTip('Decrease Volume')
        minsV_button.move(200,110)
        minsV_button.clicked.connect(self.minsV_button)
 
        stop_button=QPushButton('Stop',self)
        stop_button.setToolTip('Stop Song')
        stop_button.move(300,110)
        stop_button.clicked.connect(self.stop_button)

        info_button=QPushButton('Song Details',self)
        info_button.setToolTip('Get Song Details')
        info_button.move(400,110)
        info_button.clicked.connect(self.info_button)
    #play button handler    
    def play_button(self):
        print("Playing Music")
        if self.Playlist.mediaCount()==0:
            self.file_dialog()
        elif self.Playlist.mediaCount()!=0:
            self.button_stat=1
            self.Player.play()

    #pause button handler
    def pause_button(self):
        print("Pause Music")
        self.button_stat=2
        self.Player.pause()

    #prev button handler
    def prev_button(self):
        print("Next Song")
        if self.Playlist.mediaCount()==0:
            self.file_dialog()
        elif self.Playlist.mediaCount!=0:
            self.Player.playlist().previous()

    #next button handler
    def next_button(self):
        print("Prev Song")
        if self.Playlist.mediaCount()==0:
            self.file_dialog()
        elif self.Playlist.mediaCount()!=0:
            self.Player.playlist().next()
            
    #info button handler

    def info_button(self):
        print("\n  info button")
        song=eyed3.load(self.song_path)
        artist=song.tag.artist
        album=song.tag.album
        title=song.tag.title
        
        s_detail='Artist : ' +artist + '\n\tAlbum : ' + album + '\n\tTitle : ' + title 

        song_det=QMessageBox(self)
        song_det.setWindowTitle('Song Details')
        song_det.setText(s_detail)
        song_det.show()

    #volume button handler
    def plusV_button(self):
        print("Plus Volume")
        vol_ = self.Player.volume()
        vol_ = min(100,vol_+5)
        self.Player.setVolume(vol_)

    
    def minsV_button(self):
        print("Minus Volume")
        vol_ = self.Player.volume()
        vol_ = max(100,vol_-5)
        self.Player.setVolume(vol_)

    #stop button handler
    def stop_button(self):
        print("Stopping Music")
        self.button_stat=3
        self.Player.stop()
        self.Playlist.clear()
        self.statusBar().showMessage("Music Stopped")


    #open file dialog

    def open_file(self):
        fopen_button=QAction('Open File',self)
        #fopen_button.setShortcut('CTRL+O')
        fopen_button.setStatusTip('Open Music File')
        fopen_button.triggered.connect(self.file_dialog)
        return fopen_button

    #EXIT button handler

    def exit_button(self):
        exit_Button=QAction('Exit',self)
        #exit_Button.setShortcut('CTRL+Q')
        exit_Button.setStatusTip('Exit Application')
        exit_Button.triggered.connect(self.close_msg)
        return exit_Button

    def show_qoute(self,q_path):
       
        q_img=Image.open(q_path)
        q_img.show()
    def song_play(self,song_path):
        self.button_stat=1
        self.Playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.song_path)))
        self.Player.setPlaylist(self.Playlist)
        self.Player.setVolume(50)
        self.Player.play()
    
    #file dialog handler
    def file_dialog(self):
        fName=QFileDialog.getOpenFileName(self,"Select A Song","~","All Files (*) ;;  Mp3 Files(*.mp3)")
        
        if fName[0]== '' :
         print("No file Selected")

        elif self.Playlist.mediaCount()==0:
            #print(QUrl(fName[0]))

            self.song_path=fName[0]
            self.button_stat=1
            self.Playlist.addMedia(QMediaContent(QUrl.fromLocalFile(fName[0])))
            self.Player.setPlaylist(self.Playlist)
            self.Player.setVolume(50)
            self.Player.play()
             
        else:

            self.Playlist.addMedia(QMediaContent(QUrl(fName[0])))

    #close/exit handler
    def close_msg(self):
        msg=QMessageBox.question(self,'Close Msg','Click Yes to Close',QMessageBox.Yes,QMessageBox.No)

        if msg==QMessageBox.Yes:
            self._obj.change_f(1)
            self.close()
            print('Closing App')
        else:
            print('Not Closing')
            
    #status  handler
    def status_bar(self):
        self.statusBar().showMessage('ViAna Music Player')


#main
if __name__=='__main__':
    try:
    
        music_app
    except:
        music_app = QApplication(sys.argv)
        _ex = Music_App()
        sys.exit(music_app.exec())
