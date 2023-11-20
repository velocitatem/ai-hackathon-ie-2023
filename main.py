from clai import *
import os
# load .env
from dotenv import load_dotenv
load_dotenv()


# ct = extract_data(test_file)
# print(ct)



directory = "data_0611"
output_filename = "output.csv"
stack = []
for ff in get_all_files():
    # chek if file exists
    if os.path.exists(directory + "/" + ff):
        print(ff)
        ct = extract_data(ff)
        print(ct)
        stack.append(ct.dict())
        betas_to_csv(stack, output_filename)






betas_to_csv(stack, output_filename)
# cs = betas_to_csv([ts.dict()])
# print(cs)
