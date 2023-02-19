from PyQt5.QtWidgets import QApplication,QLabel ,QComboBox, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QStyle, QSlider, QFileDialog 
from PyQt5.QtGui import QIcon 
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl 
import sys

class Window(QWidget): 
    """create window display and set window icon, title, appearing position, width, height, finally display it"""
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("video-player-icon-15.ico"))
        self.setWindowTitle("PyMedia Player") 
        self.setGeometry(500, 100, 700, 500)

        self.setStyleSheet("background-color: LightBlue")

        self.create_MediaPlayer()

    def create_MediaPlayer(self): 
        """create media player with buttons: open file, play/pause, playback speed, slider and create vertical 
        and horizontal to add those buttons for displaying in window"""
        
        self.videowidget = QVideoWidget()

        self.media_Player = QMediaPlayer()

        #playBack_speed button
        self.playBack_speed = [0.5, 1.0, 1.5, 2.0]
        self.playBack_speed_label = ['0.5x', '1.0x', '1.5x', '2.0x']
        self.playBack_speed_combo = QComboBox(self)
        self.playBack_speed_combo.addItems(self.playBack_speed_label)
        self.playBack_speed_combo.setCurrentIndex(self.playBack_speed.index(1.0))
        self.playBack_speed_combo.currentIndexChanged.connect(self.set_playBack_speed)

        #fullscreen button
        self.fullscreen_button = QPushButton()
        self.fullscreen_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
        self.fullscreen_button.clicked.connect(self.set_fullscreen)

        #Pic in pic button
        self.Check = False
        self.pic_in_pic_button = QPushButton()
        self.pic_in_pic_button.setIcon(QIcon('pip.ico'))
        self.pic_in_pic_button.clicked.connect(self.pic_in_pic_mode)

        #open file button
        self.openBtn = QPushButton('Open Video') 
        self.openBtn.setStyleSheet("background-color: white; color: blue; border-color: green;") 
        self.openBtn.clicked.connect(self.open_file) 

        #play button
        self.playBtn = QPushButton() 
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video) 

        #slider
        self.slider = QSlider(Qt.Horizontal) 
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)

        hbox = QHBoxLayout() 
        hbox.setContentsMargins(0,0,0,0) 
        hbox.addWidget(self.openBtn) 
        hbox.addWidget(self.playBtn) 
        hbox.addWidget(self.slider)
        hbox.addWidget(QLabel('Playback speed: '))
        hbox.addWidget(self.playBack_speed_combo)
        hbox.addWidget(self.fullscreen_button)
        hbox.addWidget(self.pic_in_pic_button)

        vbox = QVBoxLayout() 
        vbox.addWidget(self.videowidget)
        vbox.addLayout(hbox) 

        self.media_Player.setVideoOutput(self.videowidget) 

        self.setLayout(vbox) 

        self.media_Player.stateChanged.connect(self.mediastate_changed) 
        self.media_Player.positionChanged.connect(self.position_changed) 
        self.media_Player.durationChanged.connect(self.duration_changed)

    def open_file(self): 
        """Open file media to select and display video"""
        filename, _ = QFileDialog.getOpenFileName(self, "Open video") 

        if filename != '':
            self.media_Player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

    def play_video(self): 
        """Check if it is currently playing media"""
        if self.media_Player.state() == QMediaPlayer.PlayingState:
            self.media_Player.pause()
        else:
            self.media_Player.play()

    def mediastate_changed(self): 
        """to change icon of play button to pause icon and pause icon to play"""
        if self.media_Player.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position): 
        """to set the value of the slider to the specified position argument."""
        self.slider.setValue(position) 

    def duration_changed(self, duration):
        """to create the movement of slider in media player"""
        self.slider.setRange(0, duration)

    def set_position(self, position):
        """to change the current position of the media playback to the specified value."""
        self.media_Player.setPosition(position) 

    def set_playBack_speed(self, index):
        """get the playback speed index and change speed of video in media player"""
        playBack_speed = self.playBack_speed[index]
        self.media_Player.setPlaybackRate(playBack_speed)

    def set_fullscreen(self):
        """check if screen is full or not and running full screen function"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def pic_in_pic_mode(self):
        """basically change size of media player window"""
        if self.Check == False:
            self.setGeometry(500, 100, 200, 300)
            self.Check = True
        else:
            self.setGeometry(500, 100, 700, 500)
            self.Check = False

