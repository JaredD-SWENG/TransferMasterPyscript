# Client.py is the run the client-facing logic of TransferMaster (Pyscript)

"""Necessary imports including custom module from backend.py, 
and custom functions from api.js (via import js)"""
import asyncio
from backend import get_comparer, get_syllabus
from js import alert, document, Object, window, parse_doc
from pyodide import create_proxy, to_js


"""Used to clear HTML elements"""


def clear_data():
    document.getElementById("filename").innerHTML = ''
    document.getElementById("filesize").innerHTML = ''
    document.getElementById('content').contentDocument.body.innerText = ''


"""Asynchronous Python function for file selection"""


async def file_select(event):
    # Note: print() does not work in event handlers

    clear_data()

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

        document.getElementById(
            'content').contentDocument.body.innerText = content

        '''Parsed document from file's bytes, needs to be converted to py
        because parse_doc is a js function'''
        parsed_doc = (await parse_doc(content)).to_py()

        '''psu and external of type Syllabus defined in backend.py.
        There are retrieved through the get_syllabus accessor function
        (also defined backend.py)'''
        psu = await get_syllabus(parsed_doc)
        external = await get_syllabus(parsed_doc)

        '''Any attribute of a syllabus can be easily accessed due to the
        Syllabus class. For usage examples, see: 
        https://colab.research.google.com/drive/1WTliNpWSGZE-SnPGKCJ_uo5Z9xH1SXeP.
        As of now, you need to Inspect->Console to see output.
        Note: there are slight differences between the class definition in the
        link above, but usage is not effected.'''
        print(psu.institution)

        '''Weights are being preset'''
        learning_outcomes_weight = 0.6
        textbook_weight = 0.4
        weights = [learning_outcomes_weight,
                   textbook_weight]  # send this to Comparer

        '''comparer is of type Comparer defined in backend.py.
        Accessed through get_comparer (aslo defined in backend.py)
        Only one instance of the Comparer class needs to be used.'''
        comparer = await get_comparer(psu, external, weights)

        '''Attributes of the comparer can also be easily accessed due to the 
        Comparer class. For usage examples, see: 
        https://colab.research.google.com/drive/1WTliNpWSGZE-SnPGKCJ_uo5Z9xH1SXeP.
        Note: there are slight differences between the class definition in the
        link above, but usage is not effected.'''
        print(comparer.final_score)

"""Async function that, as of now, runs the entire prototype; 
from file selection, to extraction, to comparison. Will need to 
be broken down in the future."""


async def setup_button():
    '''Python proxy for the callback function'''
    file_select_proxy = create_proxy(file_select)

    '''Setting the listener to the callback'''
    document.getElementById("file_select").addEventListener(
        "click", file_select_proxy, False)


setup_button()
