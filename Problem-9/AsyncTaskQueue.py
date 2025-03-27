import asyncio
import random
import os 

class new_task:
    def __init__(self, id_, df):
        model_id = id_
        dataframe = df

async def consumer(queue: asyncio.Queue):
    while True:
        task = await queue.get()
        model_id, input_df = get_model_data(task)
        model_loaded = load_model(model_id)
        output_prediction = None
        if model_loaded:
            output_prediction = model_loaded.predict(input_df)
            print(f"Worker finished his job {task}")
        else:
            print(f"Worker couldn't finish his job {task}")

        send_prediction_to_external_source(output_prediction, model_id)

    # This is producer which has input dataframe and model id
async def producer(queue: asyncio.Queue):

    while True:
        task = await get_task_from_external_source()
        await asyncio.sleep(0.01)
        await queue.put(task)
        print(f"Worker produced a job {task} and put into queue")

async def load_model(model):
    model_dir = os.environ.get('MODEL_PATH')
    file_path = model_dir+"/"+str(model)+".joblib"
    if os.path.exists(file_path):
        m = load(file_path)
    else:
        return None
    
async def get_model_data(task):

    return task.model_id, task.data_df

async def get_task_from_external_source():
    model_id = dummy_id
    new_df = dummy_df
    task = new_task(model_id, new_df) 
    return task

async def send_prediction_to_external_source(predicted_value, id_):
    pass

async def main():
    queue = asyncio.Queue()

    workers = asyncio.create_task(consumer(queue))
    producers = asyncio.create_task(producer(queue))
    
    tasks = [workers, producers]
    await asyncio.gather(*tasks)

asyncio.run(main())