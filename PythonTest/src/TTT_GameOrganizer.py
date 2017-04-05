class TTT_GameOrganizer:

    act_turn=0
    winner=None

    def __init__(self,px,po,nplay=1,showBoard=True,showResult=True,stat=100):
        self.player_x=px
        self.player_o=po

