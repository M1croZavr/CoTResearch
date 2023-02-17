from pathlib import Path
import requests


train_data_url = 'https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/train.jsonl'
test_data_url = 'https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/test.jsonl'


if __name__ == '__main__':
    train_data_path = Path('../GSM8K_data/train_data.jsonl')
    with open(train_data_path, mode='w+') as file:
        file.write(requests.get(train_data_url).text)

    test_data_path = Path('../GSM8K_data/test_data.jsonl')
    with open(test_data_path, mode='w+') as file:
        file.write(requests.get(test_data_url).text)
