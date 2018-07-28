import sys
from modules.NgChecker import NgChecker


def lambda_handler(event, context):
    target = event['target']
    checker_obj = NgChecker('./ng_words.txt')
    return checker_obj.get_ng_part(target)


if __name__ == '__main__':
    target = sys.argv[1]
    print(lambda_handler({'target': target}, None))
