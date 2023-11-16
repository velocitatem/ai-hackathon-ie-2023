from pydantic import BaseModel, Field
import pandas as pd
from typing import List, Optional
import json
from langchain.document_loaders import PyPDFLoader

class Beta(BaseModel):
    Isin: str
    Issuer: str
    Ccy: str = Field(..., description="Currency of the product. Ex: 'EUR' Only 3 letter acronyms are allowed")
# ["SX5E", "UKX", "SPX"]
    Underlying: List[str] = Field(..., min_items=1, max_items=5,
                                  description="Underlying(s) of the product. Ex: ['SX5E', 'UKX', 'SPX']")
    Strike: List[float] = Field(..., min_items=1, max_items=5, description="Strike of the product. Also possibly reffered to 'Strike Level'")
    Launchdate: str = Field(..., description="Launch date of the product. Ex: '31/12/2021' in the format 'dd/mm/yyyy'. It could also be called 'Initial Valuation Date'")
    Finalvalday: Optional[str] = Field(..., description="Final valuation day of the product. Ex: '31/12/2022' in the format 'dd/mm/yyyy'")
    Maturity: str = Field(..., description="Maturity of the product. Ex: '31/12/2023' in the format 'dd/mm/yyyy'")
    # optional
    Cap: Optional[int] = Field(..., description="Cap of the product. Ex: 130. This will quite probably not be included")
    Barrier: int = Field(..., description="Barrier of the product. Ex: 70 in PERCENTAGE. It could also be called 'Knock-in Larrier'. Possibly written as a multiplier of the initial price.")

    # if someonething is missing its None



def betas_to_csv(items):
    """
    Example:
    File name	Isin	Issuer	Ccy	Underlying(s)					Strike					Launch Date	Final Val. Day	Maturity	Cap	Barrier
    AB3ZFW - RBC 18-Month EUR Twin Win Autocallable on Societe Generale SA.pdf	XS1878076543	RBC	EUR	GLE					33.164					11/01/2022	11/07/2023	18/07/2023		70
    ---
    Reserver 5 columns for Underlying(s) and Strike
    """
    # df based on Beta object
    string = "File name,Isin,Issuer,Ccy,Underlying(s),,,,,Strike,,,,,Launch Date,Final Val. Day,Maturity,Cap,Barrier\n"
    for item in items:
        if item is None:
            string+=",,,,,,,,,,,,,,,,,,,\n"
            continue
        csv_line = ""
        csv_line += item["Isin"] + ".pdf,"
        csv_line += item["Isin"] + ","
        csv_line += item["Issuer"] + ","
        csv_line += item["Ccy"] + ","
        # underlying can be up to 5, leave 5 columns for it, fill with empty string if not enough
        csv_line += ",".join([str(i) for i in item["Underlying"]]) + ","
        # empty fields for Underlying(s)
        csv_line += "," * (4 - len(item["Underlying"])) + ","
        # strike can be up to 5, leave 5 columns for it, fill with empty string if not enough
        csv_line += ",".join([str(i) for i in item["Strike"]]) + ","
        # empty fields for Strike
        csv_line += "," * (4 - len(item["Strike"])) + ","
        csv_line += item["Launchdate"] + ","
        csv_line += item["Finalvalday"] + ","
        csv_line += item["Maturity"] + ","
        csv_line += str(item["Cap"]) + ","
        csv_line += str(item["Barrier"])
        string += csv_line + "\n"
    # save to csv
    with open("beta.csv", "w") as f:
        f.write(string)
    return "beta.csv"





import re
def extract_data(file_name):
    path = "./data_0611/" + file_name
    loader = PyPDFLoader(path)
    data=loader.load()
    # TODO Check with regex
    seen = set()
    raw = ""
    for page in data:
        # TODO Check with regex if not in seen and in page
        # we just add to raw because its important
        shouldAdd = True
        for i in seen:
            if i in page.page_content:
                shouldAdd = False
                break
        if shouldAdd:
            seen.add(page.page_content)
        raw += page.page_content
    raw = raw.replace("\n", " ")

    from openai import OpenAI
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are a helpful assistant to a financial advisor where you extract accurate data from a document and fill in a form. Take a deep breath and think carefully and step by step."},
        {"role": "user", "content": "I need to fill in a form for a structured product. The structure is given by the following json:" + Beta.schema_json(indent=2)},
        {"role": "system", "content": Beta.schema_json(indent=2)},
        {"role": "user", "content": "The document is the following:"},
        {"role": "system", "content": raw},
        {"role": "user", "content": "Just to remind you the format is the following:\n" + Beta.schema_json(indent=2)},
        {"role": "system", "content": "Return the data as a JSON that is key~value pairing not a schema. Make sure to pay attention to how the keys are spelled. My boss is very strict about it and my career depends on it. Go."},
    ],
    response_format={ 'type': "json_object" }
    )

    print(completion.choices[0].message)
    # save json to file
    ct = json.loads(completion.choices[0].message.content)
    for k, v in ct.items():
        if v == "":
            # replace with expected type 0 or "" or []
            if k in ["Cap", "Barrier"]:
                ct[k] = 0
            else:
                ct[k] = None
    if pd.isnull(ct["Cap"]):
        ct["Cap"] = 0
    if pd.isnull(ct["Barrier"]):
        ct["Barrier"] = 0
    # other possible fails are Underlying(s) and Strike
    if ct["Underlying"] == "":
        ct["Underlying"] = []
    if ct["Strike"] == "":
        ct["Strike"] = []
    ct = Beta(**ct)
    return ct


def get_all_files():
    truePath = "./data_0611/ground_truth_0611.xlsx"
    trueData = pd.read_excel(truePath)
    return trueData["File name"].tolist()



def entry_to_object(entryName):

    import pandas as pd
    truePath = "./data_0611/ground_truth_0611.xlsx"
    trueData = pd.read_excel(truePath)
    ctFile = entryName

    exp=trueData[trueData["Isin"] == ctFile.split(".")[0]]
    exp=exp.to_dict(orient="records")[0]
    # rename columns
    exp["Launchdate"] = exp.pop("Launch Date")
    exp["Finalvalday"] = exp.pop("Final Val. Day")

    # convert Underlying(s) and all following Unnamed columns to list
    exp["Underlying"] = [exp["Underlying(s)"], exp["Unnamed: 5"], exp["Unnamed: 6"], exp["Unnamed: 7"], exp["Unnamed: 8"]]
    exp["Strike"] = [exp["Strike"], exp["Unnamed: 10"], exp["Unnamed: 11"], exp["Unnamed: 12"], exp["Unnamed: 13"]]
    exp.pop("Underlying(s)")
    [exp.pop(k) for k in ["Unnamed: 5", "Unnamed: 6", "Unnamed: 7", "Unnamed: 8", "Unnamed: 10", "Unnamed: 11", "Unnamed: 12", "Unnamed: 13"]]
    # replace empty string with 0 if the column is Cap or Barrier
    # remove nan in Underlying(s) and Strike list
    for k, v in exp.items():
        if v == "":
            # replace with expected type 0 or "" or []
            if k in ["Cap", "Barrier"]:
                exp[k] = 0
            else:
                exp[k] = None
        elif k in ["Underlying", "Strike"]:
            exp[k] = [i for i in v if pd.notnull(i)]
        # timestamps to str
        elif isinstance(v, pd.Timestamp):
            exp[k] = v.strftime("%d.%m.%Y")
    # make sure Cap is not nan
    if pd.isnull(exp["Cap"]):
        exp["Cap"] = 0
    exp = Beta(**exp)
    return exp
