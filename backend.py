# Backend.py runs the backend logic of TransferMaster (Pyscript)

import asyncio
import json
#import js
from js import query
from pyodide.http import pyfetch, FetchResponse
from pyodide import to_js
from typing import Optional, Any
import numpy as np
from statistics import mean

"""For usage examples on the Syllabus class, see: 
https://colab.research.google.com/drive/1WTliNpWSGZE-SnPGKCJ_uo5Z9xH1SXeP.
Note: there are slight differences between the class definition in the
link above, but usage is not effected."""


class Syllabus:
    """Class to represent a syllabus"""

    def init_institution(self, doc) -> None:
        """If institution is available, initialize it"""

        if (doc['data']['institution']) != None:
            self.institution = doc['data']['institution']['name']

    def init_course(self, doc) -> None:
        """If course is available, initialize it"""

        # where the item is held
        course_holder = np.array(doc['data']['extracted_sections']['title'])

        if course_holder.size != 0:  # empty array will have size 0
            self.course = doc['data']['extracted_sections']['title'][0]['text']

    def init_credits(self, doc) -> None:
        """If credits is available, initialize it"""

        credits_holder = np.array(doc['data']['extracted_sections']['credits'])

        if credits_holder.size != 0:
            self.credits = doc['data']['extracted_sections']['credits'][0]['text']

    def init_textbook(self, doc) -> None:
        """If textbook is available, initialize it"""

        textbook_holder = np.array(
            doc['data']['extracted_sections']['required_reading'])

        if textbook_holder.size != 0:
            self.textbook = doc['data']['extracted_sections']['required_reading'][0]['text']

    def init_learning_outcomes(self, doc) -> None:
        """If learning outcomes are available, initialize it"""

        learning_outcomes_holder = np.array(
            doc['data']['extracted_sections']['learning_outcomes'])

        if learning_outcomes_holder.size != 0:

            # number of learning outcomes
            num_outcomes = len(
                doc['data']['extracted_sections']['learning_outcomes'])

            for i in range(num_outcomes):
                self.learning_outcomes.append(
                    doc['data']['extracted_sections']['learning_outcomes'][i]['text'])

    def __init__(self, document) -> None:
        """If given document is a syllabus, initialize it"""

        self.syllabus = False  # whether the document is a syllabus
        self.institution = ''
        self.course = ''
        self.credits = 0
        self.textbook = ''
        self.learning_outcomes = []

        if (document['data']['syllabus_probability'] > 0.90):  # threshold is 90%
            self.syllabus = True
            self.init_institution(document)
            self.init_course(document)
            self.init_credits(document)
            self.init_textbook(document)
            self.init_learning_outcomes(document)


"""Getter for Syllabus"""


async def get_syllabus(parsed_doc) -> Syllabus:
    return Syllabus(parsed_doc)


"""For usage examples on the Comparer class, see: 
https://colab.research.google.com/drive/1WTliNpWSGZE-SnPGKCJ_uo5Z9xH1SXeP.
Note: there are slight differences between the class definition in the
link above, but usage is not effected."""

# list of outputs for 1 objective (needs to be outside Comparer class, but don't ask why)
output = []


class Comparer:
    """Class that compares 2 syllabi"""

    source_syllabus = None  # source syllabus has it objectives as the source sentences
    other_syllabus = None
    # (final) percentage match for the learning outcomes
    learning_outcomes_comparison_percentage = 0.0
    textbook_comparison_percentage = 0.0  # percentage match for textbook
    final_score = 0.0

    async def get_individual_comparisons(self, index) -> list:
        """Get the percentage matches for each objective in the source syllabus"""

        individual_comparison_percentages = []  # for each objective in source syllabus

        source = self.source_syllabus.learning_outcomes[index]  # 1 from source
        other = self.other_syllabus.learning_outcomes  # all from other syllabus

        # this async call permeates this entire class (follow the awaits)
        # other is converted to js, and then output is converted back to py
        output = (await query(source, to_js(other))).to_py()

        for o in output:
            if o > 0.35:  # thershold is 0.35 (lose items less than threshold)
                individual_comparison_percentages.append(o)

        return individual_comparison_percentages

    async def get_grouped_comparisons(self) -> None:
        """Get all the individual comparison percentages and group them"""

        for i in range(2):  # eventually change 2 to len(self.source_syllabus.learning_outcomes)
            individual_comparison_percentages = await self.get_individual_comparisons(i)
            # if an entire objective had no match, 0 it
            if len(individual_comparison_percentages) == 0:
                self.grouped_comparison_percentages.append([0])
            else:
                self.grouped_comparison_percentages.append(
                    individual_comparison_percentages)

    async def get_learning_outcomes_percentage(self) -> None:
        """Get the learning outcomes match percentage"""

        await self.get_grouped_comparisons()

        averages = []

        for i in self.grouped_comparison_percentages:  # get averages
            averages.append(mean(i))

        self.learning_outcomes_comparison_percentage = mean(
            averages)  # get average of averages
        # send to items for final score
        self.items_to_compare.append(
            self.learning_outcomes_comparison_percentage)

    def get_textbook_comparison_percentage(self) -> None:
        """Get the textbook match percentage"""

        if ((self.source_syllabus.textbook) != '' and (self.other_syllabus.textbook) != ''):  # if both have a textbook
            self.textbook_comparison_percentage = 1.0

        # send to items for final score
        self.items_to_compare.append(self.textbook_comparison_percentage)

    def get_final_score(self, items, weights) -> None:
        """Get the final score based on items and their respective weights"""

        for i in range(len(items)):
            self.final_score += (items[i] * weights[i])  # weighted average

    async def create(source_syllabus, other_syllabus, item_weights):
        """Create function replaces init because init cannot be async"""

        self = Comparer()
        # 2D list of group of individual_comparison_percentages
        self.grouped_comparison_percentages = []
        self.items_to_compare = []  # percentages being sent into final score
        self.item_weights = []  # wieghts being sent into final score
        self.source_syllabus = source_syllabus
        self.other_syllabus = other_syllabus
        self.item_weights = item_weights
        await self.get_learning_outcomes_percentage()
        self.get_textbook_comparison_percentage()
        self.get_final_score(self.items_to_compare, self.item_weights)
        return self


"""Getter for Comparer"""


async def get_comparer(source_syllabus, other_syllabus, weights) -> Comparer:
    return await Comparer.create(source_syllabus, other_syllabus, weights)


"""These functions are not currently in use, but may have potential in future"""

# async def request(url: str, method: str = "POST", body: Optional[str] = None,
#                   headers: Optional[dict[str, str]] = None, **fetch_kwargs: Any) -> FetchResponse:
#     """
#     Async request function. Pass in Method and make sure to await!
#     Parameters:
#         url: str = URL to make request to
#         method: str = {"GET", "POST", "PUT", "DELETE"} from `JavaScript` global fetch())
#         body: str = body as json string. Example, body=json.dumps(my_dict)
#         headers: dict[str, str] = header as dict, will be converted to string...
#             Example, headers=json.dumps({"Content-Type": "application/json"})
#         fetch_kwargs: Any = any other keyword arguments to pass to `pyfetch` (will be passed to `fetch`)
#     Return:
#         response: pyodide.http.FetchResponse = use with .status or await.json(), etc.
#     """
#     kwargs = {"method": method,
#               "mode": 'no-cors'}  # CORS: https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
#     kwargs["body"] = body
#     kwargs["headers"] = headers
#     kwargs.update(fetch_kwargs)

#     response = await pyfetch(url, **kwargs)
#     return response


# api_token = '9c263dc72cfcf24432a1ae9acdab709c55ba14f4'  # API access token


# # post the syllabus as a stream of bytes to the api
# async def parse_doc(data: bytes):
#     res = await request(url='https://parser-api.opensyllabus.org/v1/', body=data, headers={'Authorization': f'Token {api_token}'})
#     return res.json()

# Sentence transformer api
#API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
#API_TOKEN = "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"
#headers = {"Authorization": f"Bearer {API_TOKEN}"}

# async def query(payload):
#   response = await request(API_URL, body=json.dumps(payload), headers=headers, method="POST")
#  return response.json()
