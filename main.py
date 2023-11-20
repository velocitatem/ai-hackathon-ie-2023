from clai import *
import argparse
import os
# load .env
from dotenv import load_dotenv
load_dotenv()


# ct = extract_data(test_file)
# print(ct)


def docall(directory, output_name, gpt4=False):
    stack = []
    targets = [fn for fn in os.listdir(directory) if fn.lower().endswith('.pdf')]
    for filename in sorted(targets):
        pdf_path = os.path.join(filename)
        print("Getting ", pdf_path)
        data = extract_data(pdf_path, gpt4)
        stack.append(data.dict())
        if data is not None:
            betas_to_csv(stack, output_name)

    betas_to_csv(stack, output_name)



def main():
    parser = argparse.ArgumentParser(description='Extract structured product data from PDF documents.')
    parser.add_argument('dataset', type=str, help='Path to the directory containing PDF documents.')
    parser.add_argument('output_name', type=str, help='Name of the output CSV file. Ex: out.csv')
    parser.add_argument('--gpt4', action='store_true', help='Use GPT-4 instead of GPT-3.5 Turbo')

    args = parser.parse_args()

    docall(args.dataset, args.output_name, args.gpt4)

if __name__ == "__main__":
    main()
