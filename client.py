# Client.py is the run the client-facing logic of TransferMaster (Pyscript)

"""Necessary imports including custom module from backend.py,
and custom functions from api.js (via import js)"""
import asyncio
import panel as pn
import numpy as np
import matplotlib.pyplot as plt
from backend import get_comparer, get_syllabus, Syllabus
from js import alert, document, Object, window, parse_doc
from pyodide import create_proxy, to_js

# psu = Syllabus()
# external = Syllabus()
output2 = ''


"""Used to clear HTML elements"""


def clear_psu_data():
    document.getElementById("filename").innerHTML = ''
    document.getElementById("filesize").innerHTML = ''
    document.getElementById(
        'psu_institutionframe').contentDocument.body.innerText = ''
    document.getElementById(
        'psu_coursename').contentDocument.body.innerText = ''
    document.getElementById(
        'psu_credits').contentDocument.body.innerText = ''
    document.getElementById(
        'psu_textbook').contentDocument.body.innerText = ''
    document.getElementById(
        'psu_objectives').contentDocument.body.innerText = ''


def clear_ext_data():
    document.getElementById("filename").innerHTML = ''
    document.getElementById("filesize").innerHTML = ''
    document.getElementById(
        'ext_institutionframe').contentDocument.body.innerText = ''
    document.getElementById(
        'ext_coursename').contentDocument.body.innerText = ''
    document.getElementById(
        'ext_credits').contentDocument.body.innerText = ''
    document.getElementById(
        'ext_textbook').contentDocument.body.innerText = ''
    document.getElementById(
        'ext_objectives').contentDocument.body.innerText = ''


"""Asynchronous Python function for file selection"""

# removed parameter event


async def psu_file_select(event):
    # Note: print() does not work in event handlers

    clear_psu_data()

    try:
        options = {
            "multiple": False,
            "startIn": "documents"
        }

        '''fileHandle needs to wait for this File System Access API call
        (it needs "options", which is first converted to js)'''
        fileHandles = await window.showOpenFilePicker(Object.fromEntries(to_js(options)))

    except Exception as e:
        console.log('Exception: ' + str(e))
        return

    for fileHandle in fileHandles:
        file = await fileHandle.getFile()

        document.getElementById(
            "filename").innerHTML = 'File Name: ' + file.name
        document.getElementById(
            "filesize").innerHTML = 'File Size: ' + str(file.size)
        document.getElementById(
            "filetype").innerHTML = 'File Type: ' + str(file.type)
        document.getElementById(
            "filedate").innerHTML = 'File Date: ' + str(file.lastModifiedDate)

        '''File's bytes to send for parsing'''
        content = await file.arrayBuffer()

        '''document.getElementById(
            'content').contentDocument.body.innerText = content'''

        '''Parsed document from file's bytes, needs to be converted to py
        because parse_doc is a js function'''
        parsed_doc = (await parse_doc(content)).to_py()

        '''psu and external of type Syllabus defined in backend.py.
        There are retrieved through the get_syllabus accessor function
        (also defined backend.py)'''

        global psu
        psu = await get_syllabus(parsed_doc)
        # external = await get_syllabus(parsed_doc)

        '''Any attribute of a syllabus can be easily accessed due to the
        Syllabus class. For usage examples, see:
        https://colab.research.google.com/drive/1WTliNpWSGZE-SnPGKCJ_uo5Z9xH1SXeP.
        As of now, you need to Inspect->Console to see output.
        Note: there are slight differences between the class definition in the
        link above, but usage is not effected.'''
        # print(psu.institution)
        # print(psu.course)
        # print(psu.credits)
        # print(psu.textbook)
        document.getElementById(
            'psu_institutionframe').contentDocument.body.innerText = psu.institution
        document.getElementById(
            'psu_coursename').contentDocument.body.innerText = psu.course
        document.getElementById(
            'psu_credits').contentDocument.body.innerText = psu.credits
        if(psu.textbook == ''):
            text = 'Not specified'
            document.getElementById(
                'psu_textbook').contentDocument.body.innerText = text
        else:
            document.getElementById(
                'psu_textbook').contentDocument.body.innerText = psu.textbook
        for i in psu.learning_outcomes:
            document.getElementById(
                'psu_objectives').contentDocument.body.innerText += "\n" + i

        # '''Weights are being preset'''
        # learning_outcomes_weight = 0.6
        # textbook_weight = 0.4
        # weights = [learning_outcomes_weight,
        #            textbook_weight]  # send this to Comparer

        # '''comparer is of type Comparer defined in backend.py.
        # Accessed through get_comparer (aslo defined in backend.py)
        # Only one instance of the Comparer class needs to be used.'''
        # comparer = await get_comparer(psu, external, weights)

        # '''Attributes of the comparer can also be easily accessed due to the
        # Comparer class. For usage examples, see:
        # https://colab.research.google.com/drive/1WTliNpWSGZE-SnPGKCJ_uo5Z9xH1SXeP.
        # Note: there are slight differences between the class definition in the
        # link above, but usage is not effected.'''
        # print(comparer.final_score)
        # document.getElementById('finalscore').contentDocument.body.innerText = str(
        #     comparer.final_score)


async def external_file_select(event):
    # Note: print() does not work in event handlers

    clear_ext_data()

    try:
        options = {
            "multiple": False,
            "startIn": "documents"
        }

        '''fileHandle needs to wait for this File System Access API call
        (it needs "options", which is first converted to js)'''
        fileHandles = await window.showOpenFilePicker(Object.fromEntries(to_js(options)))

    except Exception as e:
        console.log('Exception: ' + str(e))
        return

    for fileHandle in fileHandles:
        file = await fileHandle.getFile()

        document.getElementById(
            "filename").innerHTML = 'File Name: ' + file.name
        document.getElementById(
            "filesize").innerHTML = 'File Size: ' + str(file.size)
        document.getElementById(
            "filetype").innerHTML = 'File Type: ' + str(file.type)
        document.getElementById(
            "filedate").innerHTML = 'File Date: ' + str(file.lastModifiedDate)

        '''File's bytes to send for parsing'''
        content = await file.arrayBuffer()

        '''document.getElementById(
            'content').contentDocument.body.innerText = content'''

        '''Parsed document from file's bytes, needs to be converted to py
        because parse_doc is a js function'''
        parsed_doc = (await parse_doc(content)).to_py()

        '''psu and external of type Syllabus defined in backend.py.
        There are retrieved through the get_syllabus accessor function
        (also defined backend.py)'''

        global external
        external = await get_syllabus(parsed_doc)
        # external = await get_syllabus(parsed_doc)

        '''Any attribute of a syllabus can be easily accessed due to the
        Syllabus class. For usage examples, see:
        https://colab.research.google.com/drive/1WTliNpWSGZE-SnPGKCJ_uo5Z9xH1SXeP.
        As of now, you need to Inspect->Console to see output.
        Note: there are slight differences between the class definition in the
        link above, but usage is not effected.'''

        # print(psu.institution)
        # print(psu.course)
        # print(psu.credits)
        # print(psu.textbook)
        document.getElementById(
            'ext_institutionframe').contentDocument.body.innerText = external.institution
        document.getElementById(
            'ext_coursename').contentDocument.body.innerText = external.course
        document.getElementById(
            'ext_credits').contentDocument.body.innerText = external.credits
        if(external.textbook == ''):
            text = 'Not specified'
            document.getElementById(
                'ext_textbook').contentDocument.body.innerText = text
        else:
            document.getElementById(
                'ext_textbook').contentDocument.body.innerText = external.textbook
        for i in external.learning_outcomes:
            document.getElementById(
                'ext_objectives').contentDocument.body.innerText += "\n" + i


'''Async function that, as of now, runs the entire prototype;
from file selection, to extraction, to comparison. Will need to
be broken down in the future.'''

# sets up psu upload button


async def setup_psu_button():
    '''Python proxy for the callback function'''
    file_select_proxy = create_proxy(psu_file_select)

    '''Setting the listener to the callback'''
    document.getElementById("psu_file_select").addEventListener(
        "click", file_select_proxy, False)

# sets up external upload button


async def setup_external_button():
    '''Python proxy for the callback function'''
    file_select_proxy = create_proxy(
        external_file_select)

    '''Setting the listener to the callback'''
    document.getElementById("external_file_select").addEventListener(
        "click", file_select_proxy, False)


compare = pn.widgets.Button(name="Compare Syllabi")
input_learning_outcomes_weight = pn.widgets.FloatSlider(
    start=0.0, end=1.0, name="Weighting for Learning Objectives")
input_textbook_weight = pn.widgets.FloatSlider(
    start=0.0, end=1.0, name="Weighting for Textbook")


async def compare_pipeline(_):
    '''Weights are being preset'''
    learning_outcomes_weight = input_learning_outcomes_weight.value
    textbook_weight = input_textbook_weight.value
    weights = [learning_outcomes_weight,
               textbook_weight]  # send this to Comparer

    '''comparer is of type Comparer defined in backend.py.
    Accessed through get_comparer (aslo defined in backend.py)
    Only one instance of the Comparer class needs to be used.'''

    global comparer
    comparer = await get_comparer(psu, external, weights)

    '''Attributes of the comparer can also be easily accessed due to the
    Comparer class. For usage examples, see:
    https://colab.research.google.com/drive/1WTliNpWSGZE-SnPGKCJ_uo5Z9xH1SXeP.
    Note: there are slight differences between the class definition in the
    link above, but usage is not effected.'''
    print(comparer.final_score)


async def setup():
    await setup_psu_button()
    await setup_external_button()

    output = pn.Column(input_learning_outcomes_weight,
                       input_textbook_weight, compare).servable()
    compare.on_click(compare_pipeline)
    pn.Row(output, output2)
    # pn.Column(pn.bind(output, compare.param.clicks)
    #           ).servable(),
    # pn.Column(compare).servable()
    # )
    print("compare_pipeline")
    # print(comparer.get_final_score)


# data visualizations


# First create the x and y coordinates of the points.


setup()
