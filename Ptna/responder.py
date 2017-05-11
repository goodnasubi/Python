import random
import re


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

    def response(self, input):
        """
        オーバーライドを前提としたresponsd()メソッド
        :param input: 入力された文字列
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

    def response(self, input):
        """
        応答文字列を作って
        :param input: 
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



    def response(self, input):
        """
        応答文字列を作って返す
        :param input: 入力された文字列
        :return: リストからランダムに抽出文字列
        """

        #return (random.choice(self.responses))

        return (random.choice(self.dictionary.random))

class PatternResponder(Responder):
    """
    パターンに反応するためのサブクラス
    """

    def response(self, input):
        """
        パターンにマッチした場合に応答文字列を作って返す
        
        :param input: 入力された文字列
        :return: 
        """
        # pattarn['pattern'] と ['phrases'] に対して反復処理
        for ptn, prs in zip(
                self.dictionary.pattern['pattern'],
                self.dictionary.pattern['phrases']
            ):
            # インプットされた文字列に対して
            # パターン(ptnの値)でパターンマッチを行う
            m = re.search(ptn, input)

            # インプットされた文字列がパターンにマッチしている場合
            if m:
                # 応答フレーズ(ptn[1])を　'|'で切り分けて
                # ランダムに1文返す
                resp  = random.choice(prs.split('|'))
                # 抽出した応答フレーズを返す
                # 応答フレーズの中の %match% が埋め込まれている場合
                # インプットされた文字列内のパターンマッチした
                # 文字列に置き換える
                return re.sub('%match%', m.group(), resp)

        # パターンマッチしない場合は、ランダム辞書から返す
        return random.choice(self.dictionary.random)
