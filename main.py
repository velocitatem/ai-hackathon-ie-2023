from clai import *
import os

test_file = "XS2358486194.pdf"
# ct = extract_data(test_file)
# print(ct)


directory = "data_0611"
stack = []
for ff in get_all_files():
    # chek if file exists
    if os.path.exists(directory + "/" + ff):
        print(ff)
        try:
            ct = extract_data(ff)
            print(ct)
            stack.append(ct.dict())
            betas_to_csv(stack)
        except Exception as e:
            print("error", e)
            stack.append(None)
            continue






betas_to_csv(stack)
# cs = betas_to_csv([ts.dict()])
# print(cs)
