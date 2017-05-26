from Ptna.responder import *
from Ptna.dictionary import *
from Ptna.analyzer import *

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
        # Emotionを生成
        self.emotion = Emotion(self.dictionary)

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
        # 機嫌値を更新
        self.emotion.update(input)
        # インプット文字列を解析
        parts = analyze(input)
        #print(parts)
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

        print(self.emotion.mood)
        # return self.responder.response(input, self.emotion.mood)
        # 応答フレーズを生成
        resp = self.responder.response(input, self.emotion.mood)
        # 学習メソッドを呼ぶ
        self.dictionary.study(input, parts)
        # 応答フレーズを返す
        return resp

    def save(self):
        """
        Dictionaryのsave()を呼ぶ中継メソッド
        :return: 
        """
        self.dictionary.save()


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


class Emotion:
    """ピティナの感情モデル"""
    # 機嫌値の上限/下限と回復値を設定
    MODE_MIN = -15
    MODE_MAX = 15
    MODE_RECOVERY = 0.5

    def __init__(self, dictionary):
        """
        Dictionary オブジェクトをdictionaryに格納
        機嫌値mode を 0 に設定
        :param dictionary: Dictionaryオブジェクト
        """
        self.dictionary = dictionary
        # 機嫌値を保持ずるインスタンス変数
        self.mood = 0

    def update(self, input):
        """
        ユーザーからの入力をパラメーターinputで受け取り
        パターン辞書にマッチさせて機嫌値を変動させる
        :param input: ユーザーからの入力
        :return: 
        """
        # パターン辞書の各行を繰り返しパターンマッチさせる
        for ptn_item in self.dictionary.pattern:
            # パターンマッチすればadjust_mode()で機嫌値を変動させる
            if ptn_item.match(input):
                self.adjust_mode(ptn_item.modify)
                break


        # 機嫌を徐々に元に戻す処理
        if self.mood < 0:
            self.mood += Emotion.MODE_RECOVERY
        elif self.mood > 0:
            self.mood -= Emotion.MODE_RECOVERY


    def adjust_mode(self, val):
        """
        機嫌値を増減させる
        :param val: 機嫌変動値
        :return: 
        """
        # 機嫌値modeの値を機嫌変動値によって増減する
        self.mood += int(val)
        # MODE_MAX と MODE_MINと比較して、機嫌値が取り得る範囲に収める
        if self.mood > Emotion.MODE_MAX:
            self.mood = Emotion.MODE_MAX
        elif self.mood < Emotion.MODE_MIN:
            self.mood = Emotion.MODE_MIN