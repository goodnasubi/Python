import random
import re
from Ptna.analyzer import *

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

    # def study(self, input):
    #     """
    #     ユーザー発言を学習する
    #     :param input: ユーザー発話
    #     :return:
    #     """
    #     # インプット文字列の改行と空白は取り除いておく
    #     input = input.rstrip('\n')
    #     # 発言がランダム辞書に存在しなければ
    #     # self.random の末尾に追加
    #     if not input in self.random:
    #         self.random.append(input)

    def study(self, input, parts):
        """
        ユーザー発言を学習する
        :param input: ユーザー発話
        :param parts 形態素解析結果
        :return: 
        """
        # インプット文字列の改行と空白は取り除いておく
        input = input.rstrip('\n')
        ## 発言がランダム辞書に存在しなければ

        # インプット文字列を引数に、ランダム辞書に登録するメソッドを呼ぶ
        self.study_random(input)
        # インプット文字列と解析結果を引数に、パターン辞書の登録メソッドを呼ぶ
        self.study_pattern(input, parts)


    def study_random(self, input):
        """
        ユーザーの発言を学習する
        :param input: ユーザーの発言
        :return: 
        """
        # 発言がランダム辞書に存在しなければ
        # self.random の末尾に追加
        if not input in self.random:
            self.random.append(input)


    def study_pattern(self, input, parts):
        """
        ユーザーの発話を学習する
        :param input: インプット文字列
        :param parts: 形態素解析の結果（リスト）
        :return: 
        """
        # 多重リストの要素を２つのパラメータに取り出す
        for word, part in parts:
            # analyzerのkeyword_check()関数による名詞チェックが、
            # trueの場合
            if (keyword_check(part)):
                depend = False # ParseItemオブジェクトを保持する変数
                # patternリストのpatternキーを反復処理
                for ptn_item in self.pattern:
                    m = re.search(ptn_item.pattern, word)
                    # インプットされた名詞が既存のパターンとマッチしたら
                    # patternリストからマッチしたParseItemオブジェクトを取得
                    if(re.search(ptn_item.pattern, word)):
                        depend = ptn_item
                        break # マッチしたら止める
                # 既存パターンとマッチしたParseItemオブジェクトから
                # add_phraseを呼ぶ
                if depend:
                    depend.add_phrase(input)
                else:
                    # 既存パターンに存在しない名詞であれば
                    # 新規のParseItemオブジェクトを
                    # patternリストに追加
                    self.pattern.append(ParseItem(word, input))




    def save(self):
        """
        self.random の内容を丸ごと辞書に書き込む
        :return: 
        """
        # 各要素の末尾に改行を追加する
        for index, element in enumerate(self.random):
            self.random[index] = element + '\n'
        # ランダム辞書に書き込む
        with open('random.txt', 'w', encoding='utf_8') as f:
            f.writelines(self.random)

        # パターン辞書ファイルに書き込むデータを保持するリスト
        pattern = []
        for ptn_item in self.pattern:
            # make_line()で行データ作成
            pattern.append(ptn_item.make_line() + '\n')
        #print('パターン辞書に書き込む最終データ', pattern)
        # パターン辞書ファイルに書き込む
        with open('pattern.txt', 'w', encoding='utf_8') as f:
            f.writelines(pattern)


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


    def add_phrase(self, phrase):
        """
        パターン辞書1行分の応答例のみを作る
        :param phrase: インプット文字列
        :return: 
        """
        # インプット文字列がphrasesリストの応答例に一致するか
        # self.phrases インプットにマッチした応答フレーズの辞書リスト
        # [ { 'need'   : 応答例の整数部分, 'phrase'   : 応答例の文字列部分 }, ... ]
        for p in self.phrases:
            # 既存の応答例に一致したら終了
            if p['phrase'] == phrase:
                return

        # phrasesリストに辞書を追加
        # { 'need'  : 0, 'phrase' : インプット文字列
        self.phrases.append({'need': 0, 'phrase' : phrase})


    def make_line(self):
        """
        パターン辞書1行分のデータを作る
        :return: 
        """
        # 必要機嫌値 + '##' + パターン
        pattern = str(self.modify) + '##' + self.pattern
        phrases = []
        for p in self.phrases:
            phrases.append(str(p['need']) + '##' + str(p['phrase']))
        return pattern + '\t' + '|'.join(phrases)
