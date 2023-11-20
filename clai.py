from pydantic import BaseModel, Field
import pandas as pd
from typing import List, Optional
import json
from langchain.document_loaders import PyPDFLoader
from openai import OpenAI

class Beta(BaseModel):
    Isin: str = Field(..., description="Unique identifier for the structured product, following the International Securities Identification Number (ISIN) format.")
    Issuer: str = Field(..., description="Name of the entity issuing the structured product. This should be the full legal name of the issuer.")
    Ccy: str = Field(..., description="The three-letter currency code representing the currency of the product, as per ISO 4217 standard. Example: 'EUR'.")
    Underlying: List[str] = Field(..., min_items=1, max_items=5, description="List of underlying assets or indices associated with the product. Provide up to five valid tickers. Example: ['SX5E', 'UKX', 'SPX'].")
    Strike: List[float] = Field(..., min_items=1, max_items=5, description="List of strike prices or levels for the product, corresponding to each underlying asset. Provide up to five values. Example: [120.5, 130.0].")
    Launchdate: str = Field(..., description="The launch or initial valuation date of the product, marking the start of its lifecycle, in 'dd/mm/yyyy' format. Example: '31/12/2021'. This date sets the initial conditions for the product.")
    Finalvalday: str = Field(None, description="The final valuation day, distinct from the maturity date, formatted as 'dd/mm/yyyy'. This is the date for the final assessment of the product's value before maturity. Example: '31/12/2022'.")
    Maturity: str = Field(..., description="The maturity date of the product, indicating its expiration and the end of its term, in 'dd/mm/yyyy' format. It's the date when final settlements are made based on the final valuation. Example: '31/12/2023'.")
    Cap: Optional[int] = Field(None, description="Optional. The upper limit or cap of the product's return, expressed as a percentage. Example: 130. Leave blank if not applicable.")
    Barrier: int = Field(..., description="The barrier level of the product, specified in percentage terms. This represents a critical price level for features like knock-in. Example: 70 (indicating 70% of the initial price).")



def betas_to_csv(items,file_name):
    beta_field_to_csv = {
        "Isin": "Isin",
        "Issuer": "Issuer",
        "Ccy": "Ccy",
        "Underlying": "Underlying(s)",
        "Strike": "Strike",
        "Launchdate": "Launch Date",
        "Finalvalday": "Final Val. Day",
        "Maturity": "Maturity",
        "Cap": "Cap",
        "Barrier": "Barrier"
    }
    import pandas as pd
    df = pd.DataFrame([i for i in items])
    df = df.rename(columns=beta_field_to_csv)
    df.to_csv(file_name, index=False)







# keywords = ['isin','issuer','ccy','currency','underlying','underlyings','strike','strikes','launch','date','dates','final valuation','day','maturity','cap','barrier','redemption','amount']
keywords = [
    'issuer', 'issuing','issuing entity', 'issuing company', 'issuing corporation', 'issuer firm', 'issuing institution',
    'currency', 'ccy', 'money','monetary', 'monetary unit', 'legal tender', 'fiat currency', 'exchange medium',
    'underlying', 'assests' 'underlying assets', 'base assets', 'core assets', 'fundamental assets',
    'strike date', 'strike day', 'exercise date', 'option strike date', 'option exercise date', 'strike',
    'final valuation date', 'last valuation date', 'ultimate valuation date', 'end valuation date',
    'launch date', 'start date', 'inception date', 'commencement date', 'beginning date', 'opening date',
    'maturity date', 'expiration date', 'expiry date', 'termination date', 'end date', 'last date', 'due date',
    'isin', 'international securities identification number', 'security identifier', 'stock identifier','instrument identifier',
    'strike', 'strikes', 'strike price', 'exercise price', 'option price', 'target price',
    'laung','launch date', 'initiation date', 'start date','inception date' 'commence launch', 'begin launch', 'inaugurate launch',
    'date', 'dates', 'day', 'days','time', 'period', 'periods', 'moment', 'calendar day',
    'final valuation', 'last valuation', 'ultimate valuation', 'final assessment', 'end valuation',
    'business day', 'trading day', 'working day',
    'cap','cap level','boundary', 'ceiling', 'limit', 'maximum', 'upper bound', 'upper limit','top level',
    'barrier', 'threshold', 'limit', 'boundary', 'obstacle', 'hindrance', 'trigger level','barrier point',
    # hard coded values
    'percent', 'max', ' x ', ' × ', 'redemption date', 'redemption amount', 'usd', 'eur', 'barrier event',
    "%"
]


import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

def count_words(text):
    words = re.findall(r'\w+', text)
    return len(words)


def count_file_words(data):
    word_count = 0
    for page in data:
        word_count += count_words(page.page_content)
    print(word_count)
    return word_count

def extract_data(file_name, gpt4=False):

    client = OpenAI()
    path = "./data_0611/" + file_name
    loader = PyPDFLoader(path)
    data=loader.load()
    #r'\b(?:\d{1,2}[-\/.]\d{1,2}[-\/.]\d{2,4}|\d{2,4}[-\/.]\d{1,2}[-\/.]\d{1,2}|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}[,.]?[-\s]*\d{2,4}|\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[,.\s]+\d{2,4})\b'

    stop_words = set(stopwords.words('english'))
    regex_pattern = r'\b(?: '+'|'.join(map(re.escape, keywords)) + r')\b|\b(?:\d{1,2}[-\/.]\d{1,2}[-\/.]\d{2,4}|\d{2,4}[-\/.]\d{1,2}[-\/.]\d{1,2}|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}[,.]?[-\s]*\d{2,4}|\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[,.\s]+\d{2,4})\b'
    seen = set()
    raw = ""

    # TODO Here hte issue is that we are minifying all the pages, which is not optimal
    # we should check if a whole document is too long, and only then minify it
    # We might be able to do this quickly with the document object but im not sure
    if count_file_words(data) < 10000:
        # pass everything to the model
        for page in data:
            hasOccurence = page.page_content is not None
            shouldAdd = hasOccurence is not None
            if shouldAdd:
                raw += page.page_content + " "
    else:
        print("Minifying")
        # trim the data
        for page in data:
            filtered_page = re.search(regex_pattern, page.page_content, re.IGNORECASE)
            hasOccurence = filtered_page is not None
            shouldAdd = hasOccurence is not None
            if shouldAdd:
                raw += page.page_content + " "


        raw = raw.replace("\n", " ")

        # add stop words
        tokenized_raw = word_tokenize(raw)
        raw = ""
        for w in tokenized_raw:
            if w not in stop_words:
                raw += w

    # for page in data:
    #     # TODO Check with regex if not in seen and in page
    #     # we just add to raw because its important
    #     filtered_page = re.search(regex_pattern, page.page_content, re.IGNORECASE)
    #     hasOccurence = filtered_page is not None
    #     print(filtered_page)

    # try rate limiting

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106" if not gpt4 else "gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant specialized in financial data analysis and extraction. Your task is to meticulously process a structured product schema and accurately populate a form with relevant data extracted from a provided document."
            },
            {
                "role": "user",
                "content": "The structured product schema is defined as follows:" + Beta.schema_json(indent=2)
            },
            {
                "role": "system",
                "content": Beta.schema_json(indent=2)
            },
            {
                "role": "user",
                "content": "Here is the document with the necessary data:"
            },
            {
                "role": "system",
                "content": raw
            },
            {
                "role": "user",
                "content": "Can you process this information and provide the data in a JSON format according to the schema? Remember, accuracy and detail are critical in this task."
            },
            {
                "role": "system",
                "content": "Analyzing the document and extracting data. I will ensure the output is accurate and aligns with the given schema, presented in a well-structured JSON format."
            }
        ],
        response_format={'type': "json_object"}
    )
    # get the status of the completion
    print(completion)

    print(completion.choices[0].message)
    # save json to file
    ct = json.loads(completion.choices[0].message.content)
    # if we have missing values, we need to fill them with nothing so pydantic can parse it

    # check if we have all the fields
    for a in Beta.__fields__:
        if a not in ct:
            ct[a] = None
    # now make sure all the lists are not empty
    for a in ["Underlying", "Strike"]:
        if ct[a] is None:
            ct[a] = []

    # if ISIN is not given or null, we make "NAN"
    if "Isin" not in ct or ct["Isin"] is None:
        ct["Isin"] = "NAN"

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
