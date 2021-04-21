import os
import re
import time
from glob import glob
from google.cloud import language_v1

# file_path = '../exp_data/tag_cleared_text/believe3/cleared_formatted_condition1_believe3.txt'
files = glob('../exp_data/tag_cleared_text/**/**.txt')

def analyze_text_sentiment(text_content):
    client = language_v1.LanguageServiceClient()

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
    return response

for file_path in files:
    with open(file_path, encoding='utf-8') as f:
        text = f.readlines()

        name = os.path.basename(os.path.dirname(file_path))
        file_name = os.path.splitext(os.path.basename(file_path))
        output_path = './sentiment_analyzed/' + name + '/sentiment_' + file_name[0] + '.txt'
        output_file = open(output_path, 'w', encoding='utf-8')

        for line_text in text:
            response = analyze_text_sentiment(line_text)
            # 文ごとの感情分析結果
            for sentence in response.sentences:
                output_file.write(u'Sentence text: {}'.format(sentence.text.content) + '\n')
                output_file.write(u'Sentence sentiment score: {}'.format(sentence.sentiment.score) + '\n')
                output_file.write(u'Sentence sentiment magnitude: {}'.format(sentence.sentiment.magnitude) + '\n')

        output_file.close()

        # 文ごとの感情分析結果
        for sentence in response.sentences:
            print(u'Sentence text: {}'.format(sentence.text.content))
            print(u'Sentence sentiment score: {}'.format(sentence.sentiment.score))
            print(u'Sentence sentiment magnitude: {}'.format(sentence.sentiment.magnitude))
