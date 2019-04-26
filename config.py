from collections import defaultdict
import operator
from functools import reduce
import pandas as pd

from figures import *


###############
# data import #
###############


def f():
    return defaultdict(f)


DATA = defaultdict(f)
with pd.HDFStore("./app_dataset.h5") as store:
    for k in store.keys():
        p = k.split("/")[1:-1]
        key = k.split("/")[-1]
        reduce(operator.getitem, p, DATA)[key] = store[k]
    PARAM_DF = store["/param_df"]

#############################################################################
# change text elements of app here (all but descriptions displayed on tabs) #
#############################################################################

HOVERTEXTS = {
    "Openness": """
        ‘Low levels of openness’ mean that companies do not have the necessary technology or desire to share more data.
        Data sharing is easier at high levels of openness, perhaps because of the use of open application programming interfaces
        like those in Open Banking.
        """,
    "Number of big companies": """
        Set the number of big companies that the model starts with.
        Big companies have many more users than their smaller rivals.""",
    "Privacy concern": """
        How much consumers are worried about privacy when they choose which company’s products to use.""",
    "Consumer preference for multiple products from the same company": """
        How much consumers like to use products from the same company - such as email and calendar -
        because doing so is easier than using products from several different companies.""",
    "Privacy shock": """
        The impact on consumers – and other companies – when a company shares personal data suddenly and unexpectedly.
        The sudden or unexpected sharing of data can cause increased consumer concern around privacy and a withdrawal of
        consent to use personal data, which can affect the company in question and other companies.
        Choose how many firms are affected by the shock. The shock will be affecting the richest companies.""",
}

DISCLAIMER = """
Disclaimer

The graphs have been produced from running the model once for each combination of inputs and are not statistically significant.
For a ‘real world’ ABM, the model would be run XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Different outcomes are possible by running the model more times, as the processes which create them are probabilistic.
The model would ideally be run many more times, creating average output values from the input choices.
"""

INTRO_MARKDOWN = """
Decision-making around data – how it is accessed, used, shared and regulated – is difficult.
We’ve been exploring different ways to make this process easier, more effective and trusted.

One technique for making better decisions could be something called ‘agent based modelling’.
This technique enables the user to bring together many different factors and conditions to analyse and better see how they affect each other.
This could therefore be useful in complex decision-making involving many different considerations – something we often encourage in data policymaking.

We’ve developed a demo of an ‘agent based model’ (ABM) to show the potential benefits and challenges of such a technique.
You can play with it, learn from it and feed back on whether this is a useful approach to policymaking.

We’ve chosen to focus this demo on one issue to illustrate how it can be used: to show the impact of
[data portability](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-data-portability/)
(the ability for individuals to obtain and reuse personal data for their own purposes across different services) across big technology companies.
We focused on this because regulation of big tech companies is very much under the spotlight, and the complex nature of the data shared by these companies is hard to build policy around.

**Introducing our ABM**

How innovative a company is in developing new products can be affected by things like how freely the company shares data and how concerned customers are by privacy issues.
Data portability and openness of data flows between companies could affect innovation in product development. You can use this agent-based model (ABM) to see how different conditions might affect how companies innovate and grow. The model results are not based on real-world data and should not be used for decision-making.

You can change the conditions in which companies are operating using the buttons on the left. Each set of changes you make produces a different result, showing what companies might do in different conditions.

Data portability and openness could affect the creation and improvement of products in many ways, and the model allows you to see:\n
* whether big companies attracting lots of consumers are being created
* how much big companies are sharing data with smaller rivals
* the rate at which new products are being created and withdrawn
* whether companies specialise in one product or several products
* the degree to which consumers choose products from one or many companies
* if products are being created in old or new categories
* the degree to which consumer preferences are being satisfied
"""

###############
# tab content #
###############

TAB_DICT = {
    "market-dominance": {
        "label": "Biggest companies",
        "store": "market_share_df",
        "figure": plot_market_concentration,
        "text": """This graph shows the proportion of all consumers using the three biggest companies’ products in a product category like such as videos or music.""",
    },
    "data-sharing": {
        "label": "Data sharing",
        "store": "data_request_plot_df",
        "figure": plot_request_distribution,
        "text": """This graph shows how many data sharing requests were granter to companies in their first year.""",
    },
    "new-products": {
        "label": "New products",
        "store": "cat_entry_and_exit_df",
        "figure": plot_market_entry,
        "text": """This graph shows firms offering new products in the product categories. Companies leave the market when they don't have enough customers or run out of money.""",
    },
    "firm-specialisation": {
        "label": "Firm specialisation",
        "store": "firm_specialisation_df",
        "figure": plot_firm_specialisation,
        "text": """This graph shows the frequency of companies making products in given product categories.""",
    },
    "complimentarity": {
        "label": "Complimentarity",
        "store": "complimentarity_df",
        "figure": plot_complimentarity,
        "text": "This graph shows the proportion of consumers purchasing products from a given number of companies in the last 12 months, with no distinction between single or multiple use.",
    },
    "category-innovation": {
        "label": "Category innovation",
        "store": "innovation_df",
        "figure": plot_new_products,
        "text": """This graph shows the number of products being developed over time, in new and existing product categories.""",
    },
    "consumer-satisfaction": {
        "label": "Consumer satisfaction",
        "store": "welfare_df",
        "figure": plot_quality_difference,
        "text": """This graph shows how well the products are satisfying consumer needs. The dots show the highest quality achieved in the product categories.""",
    },
}


################
# some styling #
################


ITEM_BOTTOM = "10px"

TOOLTIP_STYLE = {
    "background-color": "#1DD3A7",
    "font-size": 16,
    "font-family": "HelveticaNeue",
}

ABLED_STYLE_RADIO = {"display": "inline-block", "margin-right": "15px"}

DISABLED_STYLE_RADIO = {
    "color": "darkgrey",
    "display": "inline-block",
    "margin-right": "15px",
}
