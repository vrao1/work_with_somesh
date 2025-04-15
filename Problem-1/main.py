from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi import Form
from pydantic import BaseModel
import os
import openai
from typing import Annotated

def inference():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY
    if OPENAI_API_KEY is None:
        raise HTTPException(status_code=500, detail="OpenAI API key is not set")
    
    filename = 'queries_and_context.txt'

    try:
        #contents = await .read()
        fptr = open(filename, 'r')
        request_string = fptr.readlines()
        fptr.close()

        print(request_string)
        print("================================================\n")

        #print(contents)

        #context = contents
        # Update the system message with the context
        system_message = f"Hi OpenAI, How are you doing?"
        context_and_queries = f"{request_string}"
        return_val=""

        response = openai.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": context_and_queries},
            ]
        )

        return_val= return_val + "\nFor all queries, Following are the responses\n"+response.choices[0].message.content
        fname = "openai_output.html"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(return_val)

        print(return_val)
        return
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    #return {"filename": file.filename, "content": contents.decode()}

if __name__ == '__main__':
    inference()