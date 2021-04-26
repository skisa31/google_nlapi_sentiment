import os
import re
import time
from glob import glob
from google.cloud import language_v1

dir_name = input("input dir name: ")
files = glob("../exp_data/tag_cleared_text/{}/**.txt".format(dir_name))
counter = 0


def main():
    for file_path in files:
        with open(file_path, encoding="utf-8") as f:
            text = f.readlines()

            name = os.path.basename(os.path.dirname(file_path))
            file_name = os.path.splitext(os.path.basename(file_path))
            # text&score&magnitude
            output_path = "./sentiment_analyzed/{}/sentiment_{}.txt".format(
                name, file_name[0]
            )
            output_file = open(output_path, "w", encoding="utf-8")
            """
            # score only
            output_path = './sentiment_analyzed/{}/score_{}.txt'.format(
                name, file_name[0])
            output_file = open(output_path, 'w', encoding='utf-8')
            """

            print("analzying sentiment...")
            for line_text in text:
                response = analyze_text_sentiment(line_text)
                # 文ごとの感情分析結果を出力
                for sentence in response.sentences:
                    output_file.write(
                        u"Sentence text: {}\n".format(sentence.text.content)
                    )
                    output_file.write(
                        u"Sentence sentiment score: {}\n".format(
                            sentence.sentiment.score
                        )
                    )
                    output_file.write(
                        u"Sentence sentiment magnitude: {}\n".format(
                            sentence.sentiment.magnitude
                        )
                    )

            output_file.close()
        counter += 1
        print("complete {} file".format(counter))


def analyze_text_sentiment(text_content):
    client = language_v1.LanguageServiceClient()
    document = {
        "content": text_content,
        "type_": language_v1.Document.Type.PLAIN_TEXT,
        "language": "ja",
    }
    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": language_v1.EncodingType.UTF8}
    )
    return response


if __name__ == "__main__":
    main()
