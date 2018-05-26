import tkinter as tk
import tkinter.messagebox
from ptna import *
from datetime import datetime


"""グローバル変数定義
"""
entry = None            # 入力エリアのオブジェクトを保持
response_area = None    # 応答エリアのオブジェクトを保持
lb = None               # ログ表示用リストボックスを保持
action = None           # 'オプション' メニューの状態を保持
ptna = Ptna('ptna')     # Ptnaオブジェクトを保持
on_canvas = None        # Canvasオブジェクトを保持
ptyna_images = []       # イメージを保持
log = []                # インプット文字列を保持


def putlog(str):
    """
    対話ログをリストボックスに追加する関数
    :param str: 入力文字列または応答文字列
    :return: 
    """
    lb.insert(tk.END, str)
    # インプットと応答をリストlogに追加
    log.append(str + '\n')


def prompt():
    """
    ピティナのプロンプトを作る関数
    :return: 
    """
    p = ptna.name
    if (action.get())==0:
        p += ' : ' + ptna.responder.name
    return p + '> '

def chagImg(img):
    """
    画像をセットする関数
    :param img: 
    :return: 
    """
    canvas.itemconfig(
        on_canvas,
        image = ptyna_images[img]
    )

def change_looks():
    em = ptna.emotion.mood
    if -5 <= em <= 5:
        chagImg(0)
    elif -10 <= em < -5:
        chagImg(1)
    elif -15 <= em < -10:
        chagImg(2)
    elif 5 <= em <= 15:
        chagImg(3)



def talk():
    """
    対話を行う関数
    ・Ptnaクラスのdialogue() を実行して応答メッセージを取得
    ・入力文字列または応答メッセージをログに出力
    :return: 
    """
    value = entry.get()
    # 入力エリアが未入力の場合
    if not value:
        response_area.configure(text='なに？')
    # 入力されていたら対話オブジェクトを実行
    else:
        # 入力文字列を引数にしてdialogue()の結果を取得
        response = ptna.dialogue(value)
        # 応答メッセージを表示
        response_area.configure(text=response)
        # 入力文字列を引数にしてputlog()を呼ぶ
        putlog('> ' + value)
        # 応答メッセージを引数にしてputlog()を呼ぶ
        putlog(prompt() + response)
        # 入力エリアをクリア
        entry.delete(0, tk.END)

    change_looks()


def writelog():
    """
    ログファイルに辞書を更新した日時を記録
    :return: 
    """
    # 　ログを作成
    now = 'Ptna System Dialogue Log: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S' + '\n')
    log.insert(0, now)
    # ログファイルへ書き込み
    with open('log.txt', 'a', encoding='utf_8') as f:
        f.writelines(log)


#===============================================================================
# 画面を描画する関数
#===============================================================================

def run():
    # グローバル変数を使用するための記述
    global entry, response_area, lb, action, canvas, on_canvas, ptyna_images

    # メインウインドウを作成
    root = tk.Tk()
    # ウインドウのサイズを設定
    root.geometry('880x560')
    # ウインドウタイトルを設定
    root.title('Interlligent Agent : ')
    # フォントの用意
    font=('Helevetica', 14)
    font_log=('Helevetica', 11)

    def callback():
        """
        終了時の処理
        :return: 
        """
        # メッセージボックスの[OK]ボタンクリック時の処理
        if tkinter.messagebox.askyesno(
            'Quit?', 'ランダム辞書を更新していい？'
        ):
            ptna.save() # 記憶メソッド実行
            writelog()  # ログ保存
            root.destroy()
        # [キャンセル]ボタンクリック
        else:
            root.destroy()

    root.protocol('WM_DELETE_WINDOW', callback)



    # メニューバーの作成
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    # [ファイル]メニュー
    filemenu = tk.Menu(menubar)
    menubar.add_cascade(label='ファイル', menu=filemenu)
    filemenu.add_command(label='閉じる', command=callback)
    # [オプション]メニュー
    action = tk.IntVar()
    optionmenu = tk.Menu(menubar)
    menubar.add_cascade(label='オプション', menu=optionmenu)
    optionmenu.add_radiobutton(
        label='Responderを表示',       # アイテム名
        variable = action,            # 選択時の値を格納するオブジェクト
        value = 0                     # actionを0にする
    )

    optionmenu.add_radiobutton(
        label = 'Responderを表示しない',
        variable = action,
        value = 1
    )

    # キャンパスの作成
    canvas = tk.Canvas(
        root,               # 親要素をメインウインドウに設定
        width = 500,        # 幅を設定
        height = 300,       # 高さを設定
        relief = tk.RIDGE,  # 枠線を設定
        bd = 2              # 枠線の幅を設定
    )

    canvas.place(x=370, y=0)    # メインウインドウ上に設定

    # img = tk.PhotoImage(file='zunko_emote_01.gif')    # 表示するイメージを用意
    # canvas.create_image(
    #     0,                  # x座標
    #     0,                  # y座標
    #     image = img,
    #     anchor = tk.NW      # 配置の起点となる位置を左上隅に設定
    # )
    # 表示するイメージを用意
    ptyna_images.append(tk.PhotoImage(file= "talk.gif"))
    ptyna_images.append(tk.PhotoImage(file= "empty.gif"))
    ptyna_images.append(tk.PhotoImage(file= "angry.gif"))
    ptyna_images.append(tk.PhotoImage(file= "happy.gif"))

    # キャンパス上にイメージを配置
    on_canvas = canvas.create_image(
        0,                  # x座標
        0,                  # y座標
        image = ptyna_images[0],
        anchor = tk.NW      # 配置の起点となる位置を左上隅に設定
    )

    # 応答エリアを作成
    response_area = tk.Label(
        root,
        width = 50,
        height = 10,
        bg = 'yellow',
        font=font,
        relief = tk.RIDGE,
        bd = 2
    )
    response_area.place(x=370, y=305)

    # フレームの作成
    frame = tk.Frame(
        root,
        relief = tk.RIDGE,
        borderwidth = 4
    )

    def enter_key(event):
        talk()

    entry = tk.Entry(
        frame,
        width = 70,
        font = font
    )
    entry.bind("<Return>", enter_key)
    entry.pack(side = tk.LEFT)
    entry.focus_set()
    # ボタンの作成
    button = tk.Button(
        frame,
        width = 15,
        text = '話す',
        command = talk
    )
    button.pack(side=tk.LEFT)
    frame.place(x=30, y=520)


    # リストボックスを作成
    lb = tk.Listbox(
        root,
        width = 42,
        height = 30,
        font = font_log
    )
    # 縦スクロールばーを生成
    sb1 = tk.Scrollbar(
        root,
        orient = tk.VERTICAL,
        command = lb.yview      # スクロール時にListboxのyview()メソッドを呼ぶ
    )
    # 横スクロールバーを生成
    sb2 = tk.Scrollbar(
        root,
        orient = tk.HORIZONTAL,
        command = lb.xview
    )

    # リストボックスとスクロールバーを連動させる
    lb.configure(yscrollcommand = sb1.set)
    lb.configure(xscrollcommand = sb2.set)
    # grid()でリストボックス、スクロールバーを画面上に配置
    lb.grid(row = 0, column = 0)
    sb1.grid(row = 0, column = 1, sticky = tk.NS)
    sb2.grid(row = 1, column = 0, sticky = tk.EW)

    # メインループ
    root.mainloop()


#==========================================================
# プログラムの起点
#==========================================================
if __name__ == '__main__':
    run()

