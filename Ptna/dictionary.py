import random
import re

class Dictionary:
    def __init__(self):
        self.random = []
        # ランダム辞書ファイルをオープン
        rfile = open('random.txt', 'r', encoding='utf_8')
        # 各行を要素としてリストに格納
        r_lines = rfile.readlines()
        rfile.close()

        # 末尾の改行と空白文字を取り除いて、インスタンス変数に格納
        self.random = []
        for line in r_lines:
            str = line.rstrip('\n')
            if (str!=''):
                self.random.append(str)

        # パターン辞書オープン
        pfile = open('pattern.txt', 'r', encoding='utf_8')
        # 各行を要素としてリストに格納
        p_lines = pfile.readlines()
        pfile.close()
        # 末尾の改行と空白文字を取り除いて、インスタンス変数に格納
        self.new_lines = []
        for line in p_lines:
            str = line.rstrip('\n')
            if (str!=''):
                self.new_lines.append(str)
        # 辞書型のインスタンス変数を用意
        # self.pattern = {}
        # リスト型のインスタンス編巣を用意
        self.pattern = []
        # 1行をタブで切り分け
        # 'pattern'キー：正義表現のパターン
        # 'phrases'キー：応答例
        for line in self.new_lines:
            ptn, prs = line.split('\t')
            # self.pattern.setdefault('pattern', []).append(ptn)
            # self.pattern.setdefault('phrases', []).append(prs)
            self.pattern.append(ParseItem(ptn, prs))


class ParseItem:
    SEPARATOR = '^((-?\d+)##)?(.*)$'

    def __init__(self, pattern, phrases):
        """
        
        :param pattern: パターン
        :param phrases: 応答例
        """
        # 辞書のパターンの部分にSAPARATORをパターンマッチさせる
        m = re.findall(ParseItem.SEPARATOR, pattern)
        # インスタンス変数modifyに0を設定
        self.modify = 0
        # マッチ結果の整数の部分が空でなければ値の再代入
        if m[0][1]:
            self.modify = int(m[0][1])
        # インスタンス変数patternにマッチ結果のパターン部分を代入
        self.pattern = m[0][2]

        self.phrases = []   # 応用例を保持するインスタンス変数
        self.dic = {}       # インスタンス変数
        # 引数で渡された応答例を'|'で分割し、
        # 個々のy要素に対してSEPARATOR をパターンマッチさせる
        # self.phrases[ 'need'    : 応答例の整数部分
        #               'phrase'  : 応答例の文字列部分 ]
        for phrase in phrases.split('|'):
            # 応答例に対してパターンマッチを行う
            m = re.findall(ParseItem.SEPARATOR, phrase)
            # 'need' キーの値を整数部分m[0][1]にする
            # 'phrase' キーの値を応答文字列m[0][2]にする
            self.dic[ 'need' ] = 0
            if m[0][1]:
                self.dic['need'] = int(m[0][1])
            self.dic[ 'phrase' ] = m[0][2]
            # 作成した辞書をphrasesリストに追加
            self.phrases.append(self.dic.copy())

    def match(self, str):
        """
        self.pattern(各行毎の正規表現)を
        インプット文字列にパターンマッチ
        :param str: 
        :return: 
        """
        return re.search(self.pattern, str)

    def choice(self, mood):
        """
        インスタンス変数phrases(リスト)の
        ('need' 'phrase' の辞書)
        :param mode: 現在の機嫌値
        :return: 
        """
        choices = []
        # self.phrasesが保持するリストの要素(辞書)を反復処理する
        for p in self.phrases:
            # self.phrasesの'need'キーの数値と
            # パラメータmode を suitable()に渡す
            # 結果がTrueであればchoicesリストに'phrases'キーの応答例を追加
            if (self.suitable(p['need'], mood)):
                choices.append(p['phrase'])
        # choices リストが空であればNoneを返す
        if (len(choices) == 0):
            return None
        # choices リストが空でなければランダムに
        # 応答文字列を選択して返す
        return random.choice(choices)

    def suitable(self, need, mood):
        """
        インスタンス変数phrases(リスト)の
        要素('need', 'phrase'の辞書)
        :param need: 必要機嫌値
        :param mood: 現在の機嫌値
        :return: 
        """
        # 必要機嫌値が0であればTrueを返す
        if (need == 0):
            return True

        # 必要機嫌値がプラスの場合は機嫌値が必要機嫌値を超えているか判定
        elif (need > 0):
            return (mood > need)
        # 応答例の数値がマイナスの場合は機嫌値が下回っているか判定
        else:
            return (mood < need)
