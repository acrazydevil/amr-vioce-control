from flask import Flask, render_template, jsonify,request
import speech_recognition as sr
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger
import soundfile

app = Flask(__name__,static_url_path='/static')

ws_driver = CkipWordSegmenter(model="bert-base")
pos_driver = CkipPosTagger(model="bert-base")

# 路由函数，用于执行语音识别和关键字提取
@app.route('/execute_speech_recognition', methods=['POST'])
def execute_speech_recognition():
    
    audio_file = request.files['audio']
    data, samplerate = soundfile.read(audio_file)
    soundfile.write('received_audio.wav', data, samplerate, subtype='PCM_16')
    r = sr.Recognizer()

    with sr.AudioFile('received_audio.wav') as source:
        audio = r.record(source)  

    try:
        text = r.recognize_google(audio, language='zh-TW')
        print("您說的是：" + text)
    except sr.UnknownValueError:
        print("無法識別語音")
    except sr.RequestError as e:
        print("無法取得語音識別服務；{0}".format(e))
    
    ws_driver = CkipWordSegmenter(model="bert-base")
    pos_driver = CkipPosTagger(model="bert-base")
    ws = ws_driver([text])
    pos = pos_driver(ws)

    def pack_ws_pos_sentence(sentence_ws, sentence_pos):
        assert len(sentence_ws) == len(sentence_pos)
        res = []
        for word_ws, word_pos in zip(sentence_ws, sentence_pos):
            res.append(f"{word_ws}({word_pos})")
        return "\u3000".join(res)

    def extract_keywords(sentence_ws, sentence_pos, pos_tags):
        keywords = []
        for word_ws, word_pos in zip(sentence_ws, sentence_pos):
            # 只保留名詞和動詞作為關鍵字
            if word_pos in pos_tags:
                keywords.append(word_ws)
        return keywords

    for sentence, sentence_ws, sentence_pos,in zip([text], ws, pos):
        print(sentence)
        print(pack_ws_pos_sentence(sentence_ws, sentence_pos))
        # 提取名詞和動詞作為關鍵字
        place = extract_keywords(sentence_ws, sentence_pos, ['Nc'])
        things = extract_keywords(sentence_ws, sentence_pos, ['Na'])
    print(place,things)

    result = {
            'text': text,
            'place': place,
            'things':things
        }
    return jsonify(result)


# 主页路由
@app.route('/')
def index():
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
