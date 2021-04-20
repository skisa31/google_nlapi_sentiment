import os
import re
import time
from glob import glob
from google.cloud import language_v1

# file_path = '../exp_data/tag_cleared_text/believe3/cleared_formatted_condition1_believe3.txt'
files = glob('../exp_data/tag_cleared_text/**/**.txt')

client = language_v1.LanguageServiceClient()

for file_path in files:
    with open(file_path, encoding='utf-8') as f:
        text = f.readlines()

        name = os.path.basename(os.path.dirname(file_path))
        output_file = './sentiment_analyzed/' + name + '/sentiment_' + name + '.txt'

        for line_text in text:
            text_content = line_text

            document = {
                'content': text_content,
                'type_': language_v1.Document.Type.PLAIN_TEXT,
                'language': 'ja'
            }

            response = client.analyze_sentiment(
                request={
                    'document': document,
                    'encoding_type': language_v1.EncodingType.UTF8
                }
            )
        with open(output_file, 'w', encoding='utf-8') as fw:
            # 文ごとの感情分析結果
            for sentence in response.sentences:
                fw.write(u'Sentence text: {}'.format(sentence.ext.content) + '\n')
                fw.write(u'Sentence sentiment score: {}'.format(sentence.sentiment.score) + '\n')
                fw.write(u'Sentence sentiment magnitude: {}'.format(sentence.sentiment.magnitude) + '\n')

        # 文ごとの感情分析結果
        for sentence in response.sentences:
            print(u'Sentence text: {}'.format(sentence.text.content))
            print(u'Sentence sentiment score: {}'.format(sentence.sentiment.score))
            print(u'Sentence sentiment magnitude: {}'.format(sentence.sentiment.magnitude))

time.sleep(10)
