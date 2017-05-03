import random


class Responder:
    """ 応答クラスのスーパークラス
    """

    def __init__(self, name):
        """ 
        Responder オブジェクトの名前をnameに格納
        :param name: Responderオブジェクトの名前
        :return: 
        """
        self.name = name

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

    def __init__(self, name):
        """
        Responderオブジェクトのn名前を引数にして
        スーパークラスの__init__()を呼び出す
        ランダムに抽出するメッセージを格納したリストを作成
        :param name: Responderオブジェクトの名前
        """

        super().__init__(name)
        self.resposes = ['いい天気だね', '君の名はバーリーピーポー', '10円拾った']

    def response(self, input):
        """
        応答文字列を作って返す
        :param input: 入力された文字列
        :return: リストからランダムに抽出文字列
        """

        return (random.choice(self.resposes))