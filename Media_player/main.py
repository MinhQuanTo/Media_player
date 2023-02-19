import Media_player

if __name__ == '__main__':
    """Show application"""
    app = Media_player.QApplication([])
    window = Media_player.Window()
    window.show() 
    Media_player.sys.exit(app.exec())
