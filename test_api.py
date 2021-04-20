from google.cloud import language_v1

# クライアントの生成
client = language_v1.LanguageServiceClient()

# ドキュメントの生成
text_content = 'むかしむかし、あるところに、おじいさんとおばあさんが住んでいました。おじいさんは山へしばかりに、おばあさんは川へせんたくに行きました。おばあさんが川でせんたくをしていると、ドンブラコ、ドンブラコと、大きな桃が流れてきました。「おや、これは良いおみやげになるわ」おばあさんは大きな桃をひろいあげて、家に持ち帰りました。'

document = {
    'content': text_content,
    'type_': language_v1.Document.Type.PLAIN_TEXT,
    'language': 'ja'
}

# 感情分析の実行
response = client.analyze_sentiment(
    request={
        'document': document,
        'encoding_type': language_v1.EncodingType.UTF8
    })

# ドキュメントの全体の感情分析結果
print(u'Dcument sentiment score: {}'.format(response.document_sentiment.score))
print(u'Dcument sentiment magnitude: {}'.format(
    response.document_sentiment.magnitude))

# 文ごとの感情分析結果
for sentence in response.sentences:
    print(u'Sentence text: {}'.format(sentence.text.content))
    print(u'Sentence sentiment score: {}'.format(sentence.sentiment.score))
    print(u'Sentence sentiment magnitude: {}'.format(sentence.sentiment.magnitude))
