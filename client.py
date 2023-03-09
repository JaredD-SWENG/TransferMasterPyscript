# Client.py is the run the client-facing logic of TransferMaster (Pyscript)

"""Necessary imports including custom module from backend.py,
and custom functions from api.js (via import js)"""
import asyncio
import panel as pn
import numpy as np
import matplotlib.pyplot as plt
from backend import get_comparer, get_syllabus, Syllabus
from graph import graph
from js import alert, document, Object, window, parse_doc, get_summary
from pyodide import create_proxy, to_js

# psu = Syllabus()
# external = Syllabus()
# output2 = ''

"""Used to clear HTML elements and initialize to empty strings"""


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
            "startIn": "downloads"
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
            "startIn": "downloads"
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

# setting up compare button


async def setup_compare_button():
    compare = create_proxy(compare_pipeline)
    document.getElementById("compare").addEventListener("click", compare)


# #pn = panel
# # sliders
# compare = pn.widgets.Button(name="Compare Syllabi")
# input_learning_outcomes_weight = pn.widgets.FloatSlider(
#     start=0.0, end=1.0, name="Weighting for Learning Objectives")
# input_textbook_weight = pn.widgets.FloatSlider(
#     start=0.0, end=1.0, value=1.0-input_learning_outcomes_weight.value, name="Weighting for Textbook")

# file_input = pn.widgets.FileInput()


# pipeline function to send weightings and syllabi to comparer class and get final score back
async def compare_pipeline(_):
    '''Weights are being preset'''
    learning_outcomes_weight_slider = document.getElementById(
        "learning-outcomes-weight")
    textbook_weight_slider = document.getElementById("textbook-weight")

    learning_outcomes_weight = float(learning_outcomes_weight_slider.value)/100
    textbook_weight = float(textbook_weight_slider.value)/100
    weights = [learning_outcomes_weight,
               textbook_weight]  # send this to Comparer

    '''comparer is of type Comparer defined in backend.py.
    Accessed through get_comparer (aslo defined in backend.py)
    Only one instance of the Comparer class needs to be used.'''

    global comparer
    comparer = await get_comparer(psu, external, weights)

    psu_chunk = ''
    for i in psu.learning_outcomes:
        psu_chunk += i
    ext_chunk = ''
    for i in external.learning_outcomes:
        ext_chunk += i

    summary = (await get_summary(psu_chunk, ext_chunk, (round(comparer.final_score * 100, 2)))).to_py()

    fig = graph(psu.learning_outcomes, comparer.averages)
    PyScript.write('graph', fig)

    # writing final score to screen
    PyScript.write(
        "final-score", str(round(comparer.final_score * 100, 2)) + "%", append=False)
    # chatgpt summary to screen
    PyScript.write(
        "summary", summary['choices'][0]['message']['content'], append=False)

    '''Attributes of the comparer can also be easily accessed due to the
    Comparer class. For usage examples, see:
    https://colab.research.google.com/drive/1WTliNpWSGZE-SnPGKCJ_uo5Z9xH1SXeP.
    Note: there are slight differences between the class definition in the
    link above, but usage is not effected.'''
    # print(comparer.final_score)  # printed to the console
    '''once upon a time we had this pn.indicators.Number thing that's supposed to return the final score
    and apparently display it to the screen but oh well'''

# function to set up the buttons and then call the pipeline to compare and display final score

# if something goes wrong, put back async in front of each setup and the wrapper setup


async def setup():
    await setup_psu_button()
    await setup_external_button()
    await setup_compare_button()

    # output = pn.Column(input_learning_outcomes_weight,
    #                    input_textbook_weight, compare, file_input).servable()  # the sliders
    # # call function on click to print score on console
    # compare.on_click(compare_pipeline)
    # # output2 was intended to have the pn.indicator.Number thing
    # pn.Row(output, output2, file_input.value)
    # # and print it to the screen but rn it's empty
    # '''
    # # pn.Column(pn.bind(output, compare.param.clicks)
    # #           ).servable(),
    # # pn.Column(compare).servable()
    # # )
    # '''
    # print(file_input.value)  # prints "compare_pipeline"
    # # print(comparer.get_final_score)


# data visualizations


# First create the x and y coordinates of the points.
async def main():
    await setup()
    # Your other code here

if __name__ == "__main__":
    asyncio.create_task(main())
    asyncio.get_event_loop().run_forever()
