// Open Syllabus Parser API call
async function parse_doc(data)
  {
    api_token = '9c263dc72cfcf24432a1ae9acdab709c55ba14f4'
    const response = await fetch('https://parser-api.opensyllabus.org/v1/', {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Authorization': `Token ${api_token}`,
            'Content-Type': 'application/json'
        },
        body: data
    });
    return await response.json();
}


//Sentence Similarity Inference Hugging Face API call
async function query(source, other)
{
    api_token = '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'
    const response = await fetch('https://api-inference.huggingface.co/models/sentence-transformers/paraphrase-multilingual-mpnet-base-v2', {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Authorization': `Bearer ${api_token}`
        },
        body: JSON.stringify({inputs:{
            source_sentence: source,
            sentences: other
        }}) //inputs from py need to be stringified
    });
    const result = await response.json();
    return result;
}

async function get_summary()
{
    const api_key = "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";

    const response = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    },
    body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages:  [{role: "user", content: "Hello world"}],
    })
    });
    const result = await response.json();
    return result
}
    


//This function is not currently in use, but may be in

// function createObject(object, variableName){
//     //Bind a variable whose name is the string variableName
//     // to the object called 'object'
//     let execString = variableName + " = object"
//     console.log("Running '" + execString + "'");
//     eval(execString)
// }
