import random
import re
from analyzer import *


class Responder:
    """ 応答クラスのスーパークラス
    """

    def __init__(self, name, dictionary):
        """ 
        Responder オブジェクトの名前をnameに格納
        :param name: Responderオブジェクトの名前
        :return: 
        """
        self.name = name
        self.dictionary = dictionary

    def response(self, input, mood, parts):
        """
        オーバーライドを前提としたresponsd()メソッド
        :param input: 入力された文字列
        :param mood: 機嫌値
        :param parts 形態素解析結果のリスト
        :return: 空の文字列
        """
        return ""

    def get_name(self):
        """
        応答オブジェクトの名前を返す
        :return: 
        """
        return self.name


class RepeatResponder(Responder):
    """
    オウム返しのためのサブクラス
    """

    def response(self, input, mood, parts):
        """
        応答文字列を作って
        :param input: 
        :param mood: 機嫌値
        :param parts 形態素解析結果のリスト
        :return: 
        """
        return '{}ってなに？'.format(input)


class RandomResponder(Responder):
    """
    ランダムな応答オブジェクト
    """

    # def __init__(self, name):
    #     """
    #     Responderオブジェクトのn名前を引数にして
    #     スーパークラスの__init__()を呼び出す
    #     ランダム辞書をリストとして読み込んでresponsesに格納
    #     :param name: Responderオブジェクトの名前
    #     """
    #
    #     super().__init__(name)
    #     # self.resposes = ['いい天気だね', '君の名はバーリーピーポー', '10円拾った']
    #
    #     # ランダム辞書のデータをリストとして保存するインスタンス変数
    #     self.responses = []
    #     # ランダム辞書をオープン
    #     rfile = open('random.txt', 'r', encoding='utf_8')
    #     # 各行を要素とするリストを取得
    #     r_lines = rfile.readlines()
    #     rfile.close()
    #     # 末尾の改行と空白文字列を取り除いて、インスタンス変数（リスト）に格納
    #     for line in r_lines:
    #         str = line.rstrip('\n')
    #         if (str != ''):
    #             self.responses.append(str)



    def response(self, input, mood, parts):
        """
        応答文字列を作って返す
        :param input: 入力された文字列
        :param mood: 機嫌値
        :param parts 形態素解析結果のリスト
        :return: リストからランダムに抽出文字列
        """

        #return (random.choice(self.responses))

        return (random.choice(self.dictionary.random))

class PatternResponder(Responder):
    """
    パターンに反応するためのサブクラス
    """

    def response(self, input, mood, parts):
        """
        パターンにマッチした場合に応答文字列を作って返す
        
        :param input: 入力された文字列
        :param mood: 機嫌値
        :param parts 形態素解析結果のリスト
        :return: 
        """
        # pattarn['pattern'] と ['phrases'] に対して反復処理
        # for ptn, prs in zip(
        #         self.dictionary.pattern['pattern'],
        #         self.dictionary.pattern['phrases']
        #     ):
        #
        #     # インプットされた文字列に対して
        #     # パターン(ptnの値)でパターンマッチを行う
        #     m = re.search(ptn, input)
        #
        #     # インプットされた文字列がパターンにマッチしている場合
        #     if m:
        #         # 応答フレーズ(ptn[1])を　'|'で切り分けて
        #         # ランダムに1文返す
        #         resp  = random.choice(prs.split('|'))
        #         # 抽出した応答フレーズを返す
        #         # 応答フレーズの中の %match% が埋め込まれている場合
        #         # インプットされた文字列内のパターンマッチした
        #         # 文字列に置き換える
        #         return re.sub('%match%', m.group(), resp)

        self.resp = None
        for ptn_item in self.dictionary.pattern:
            # match()でインプット文字列にパターンマッチを行う
            m = ptn_item.match(input)
            # マッチした場合は機嫌値moodを引数にしてchoice()を実行、
            # 戻り値の応答文字列、またはNoneを取得
            if (m):
                self.resp = ptn_item.choice(mood)
            # choice() の戻り値がNoneでない場合は
            # 応答例の中の%match%をインプットされた文字列の
            # マッチした文字列に置き換える
            if self.resp != None:
                return re.sub('%match%', m.group(), self.resp)

        # パターンマッチしない場合は、ランダム辞書から返す
        return random.choice(self.dictionary.random)


class TemplateResponder(Responder):
    """
    テンプレートに反応するためのサブクラス
    """

    def response(self, input, mood, parts):
        """
        テンプレートを使用して応答フレーズを生成
        
        :param input: 入力された文字列
        :param mood: 機嫌値
        :param parts 形態素解析結果のリスト
        :return: 
        """

        # インプット文字列の名詞の部分のみそ格納するリスト
        keywords = []
        # テンプレート本体を格納する変数
        template = ''
        # 解析結果partsの「文字列」⇒　word, 「品詞情報」⇒　partに順次格納
        for word, part in parts:
            # 名詞であるかをチェックしてkeywordリストに格納
            if (keyword_check(part)):
                keywords.append(word)
        # keywordリストに格納された名刺の数を取得
        count = len(keywords)
        # keywordリストに１つ以上の名詞が存在し、
        # 名詞の数に対応するテンプレートが存在するかをチェック
        if (count > 0) and (str(count) in self.dictionary.template):
            # テンプレートリストから名詞の数に対応するテンプレートを
            # ランダムに抽出
            template = random.choice(self.dictionary.template[str(count)])
            # テンプレートの空欄(%noun%)に
            # keyword に格納されている名詞を埋め込む
            for word in keywords:
                template = template.replace('%noun%', word, 1)
            return template
        return random.choice(self.dictionary.random)

