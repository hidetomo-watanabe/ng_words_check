import json
import requests
import MeCab
import mojimoji
import jaconv


class NgChecker(object):
    def __init__(self, ng_words_filename):
        self.mecab_obj = MeCab.Tagger()
        self.ng_words_filename = ng_words_filename

    def _get_ng_words(self):
        f = open(self.ng_words_filename, 'r')
        ng_words = f.read().strip().split('\n')
        f.close()
        return ng_words

    def _get_ime_trans(self, text):
        response = requests.get(
            'http://www.google.com/transliterate?langpair=ja-Hira|ja&text=%s' %
            text.strip())
        return json.loads(response.text)

    def _get_morpheme_parse(self, text):
        org = self.mecab_obj.parse(text)
        result = []
        for line in org.split('\n'):
            if line == 'EOS':
                break
            word, morphemes = line.split('\t')
            # morpheme = morphemes.split(',')[0]
            base_word = morphemes.split(',')[6]
            if base_word == '*':
                result.append(word)
            else:
                result.append(base_word)
        return result

    def _trans_to_han_kata(self, text):
        hira = jaconv.hira2kata(text)
        han_hira = mojimoji.zen_to_han(hira)
        return han_hira

    def get_ng_part(self, text):
        def _is_ng(text):
            """
            # google imeが簡易形態素解析になっているため、
            # とりあえずなくす
            mecab_result = self._get_morpheme_parse(text)
            for word in mecab_result:
                word_hankata = self._trans_to_han_kata(word)
                for ng_word in ng_words_hankata:
                    if ng_word in word_hankata:
                        return True
            """
            text_hankata = self._trans_to_han_kata(text)
            for ng_word in ng_words_hankata:
                if ng_word in text_hankata:
                    return True
            return False

        check_result = []
        ng_words = self._get_ng_words()
        # 半角カタカナに統一
        ng_words_hankata = list(map(
            lambda x: self._trans_to_han_kata(x), ng_words))
        ime_result = self._get_ime_trans(text)
        # 文節ごとに処理
        for unit in ime_result:
            org = unit[0]
            trans = unit[1][0]
            if _is_ng(trans):
                check_result.append(org)
        return check_result


if __name__ == '__main__':
    pass
