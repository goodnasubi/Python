from Ptna.responder import *
from Ptna.dictionary import *

class Ptna:
    """
    ピティナの本体クラス
    """

    def __init__(self, name):
        """
        Ptnaオブジェクトの名前をnameに格納
        RandamResponderを生成して、responderに格納
        :param name: Ptnaオブジェクトの名前
        """
        self.name = name
        # self.responder = RandomResponder('Random')
        # Dictionryを生成
        self.dictionary = Dictionary()

        # RandomResponder を生成
        self.res_random = RandomResponder('Random', self.dictionary)
        # RepeatResponder を生成
        self.res_what = RepeatResponder('Repeat?', self.dictionary)
        # PatternResponder を生成
        self.res_pattern = PatternResponder('Pattern', self.dictionary)

    def dialogue(self, input):
        """
        応答オブジェクトのresponse()を呼び出して
        応答文字列を取得する
        :param input: ユーザーによって入力された文字列
        :return: 応答文字列
        """
        #return self.responder.response(input)

        # 1 から 100 をランダムに生成
        x = random.randint(0, 100)
        # 60以下ならばPatternResponderオブジェクトにする
        if x <= 60:
            self.responder = self.res_pattern
        # 61～90 以下ならばRandomResponderオブジェクトにする
        elif 61 <= x <= 90:
            self.responder = self.res_random
        # それ以外はRepeatResponderオブジェクトにする
        else:
            self.responder = self.res_what

        return self.responder.response(input)


    def get_responder_name(self):
        """
        
        :return: 応答オブジェクトの名前を返す
        """
        return self.responder.name

    def get_name(self):
        """
        
        :return: Ptna オブジェクトの名前を返す
        """
        return self.name

