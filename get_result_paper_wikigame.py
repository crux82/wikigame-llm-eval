import requests
import json
from wikigametools import get_internal_links_from_article, get_all_visible_existing_internal_links
import pandas as pd
from time import sleep
from prompts import context_with_think_last, context_with_think, context_no_think, context_types
from models import list_model
from api_key import GPT_API_KEY, LLAMA_ENDPOINT_URL
from settings import num_game_test, max_steps_try


def pairwise(iterable):
    """
    Yields consecutive pairs from the given iterable.
    Example: pairwise('ABCDEFG') → AB, BC, CD, DE, EF, FG
    """
    iterator = iter(iterable)
    a = next(iterator, None)

    for b in iterator:
        yield a, b
        a = b

def call_gpt(context, request, model):
    """
    Calls the OpenAI GPT API with the provided context, request, and model.
    Parses the response to extract a list of steps (Wikipedia page titles).
    Retries on failure.
    """
    while True:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": GPT_API_KEY
        }
        data = {
            "model": model,
            "seed": 42,
            "messages": [
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user",
                    "content": request
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        if 'choices' in response_json:
            text = response.json()['choices'][0]['message']['content']
            text_list_steps = text[text.find("###")+len("###"):].strip()
            if "@@@" in text_list_steps:
                text_list_steps = text_list_steps[:text_list_steps.find("@@@")].strip()
            list_steps = []
            for step in text_list_steps.split(" -> "):
                if step not in list_steps:
                    list_steps.append(step.strip().replace(" ", "_"))
            return list_steps
        else:
            sleep(2)
            continue


def call_gpt_link(context, request, model):
    """
    Calls the OpenAI GPT API with the provided context, request, and model.
    Parses the response to extract a list of steps (Wikipedia page titles).
    Retries on failure.
    """
    while True:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": GPT_API_KEY
        }
        data = {
            "model": model,
            "seed": 42,
            "messages": [
                {
                    "role": "system",
                    "content": context
                },
                {
                    "role": "user",
                    "content": request
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        if 'choices' in response_json:
            text = response.json()['choices'][0]['message']['content']
            text_step = text[text.find("###")+len("###"):].strip()
            if "@@@" in text_step:
                text_step = text_step.split("@@@")[0].strip()
            return text_step
        else:
            sleep(2)
            continue


def call_llama(context, request):
    """
    Calls the LLAMA endpoint with the provided context and request.
    Parses the response to extract a list of steps (Wikipedia page titles).
    """
    url = LLAMA_ENDPOINT_URL
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "richiesta": request,
        "contesto": context
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
    text = response.text
    text_list_steps = text[text.find("###")+len("###"):].strip()
    if "@@@" in text_list_steps:
        text_list_steps = text_list_steps[:text_list_steps.find("@@@")].strip()
    list_steps = []
    for step in text_list_steps.split(" -> "):
        if step not in list_steps:
            list_steps.append(step.strip().replace(" ", "_"))
    return list_steps

def call_llama_link(context, request):
    """
    Calls the LLAMA endpoint with the provided context and request.
    Parses the response to extract a list of steps (Wikipedia page titles).
    """
    url = LLAMA_ENDPOINT_URL
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "richiesta": request,
        "contesto": context
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
    text = response.text
    text_step = text[text.find("###")+len("###"):].strip()
    if "@@@" in text_step:
        text_step = text_step.split("@@@")[0].strip()
    return text_step


def check_error_steps(list_steps):
    """
    Checks the validity of each step in the provided list of steps.
    Returns a list of errors found in the path (e.g., missing links or pages).
    """
    list_steps_after = []
    list_error = []
    for prev, next in pairwise(list_steps):
        step=prev
        list_link_page = get_internal_links_from_article(prev)
        if list_link_page == False:
            continue
        else:
            if list_link_page == []:
                list_error.append(f"NO PAGE: {prev}")
            else:
                if next in list_link_page:
                    continue
                else:
                    list_error.append(f"NO LINK: {prev} -> {next}")
        list_steps_after.append(step)
    return list_error


def count_error_steps(error_steps):
    """
    Counts the number of different types of errors in the error_steps list.
    Returns the counts for missing links, missing pages, and disambiguation pages.
    """
    num_no_link = 0
    num_no_page = 0
    num_dis_page = 0
    for error in error_steps:
        if "NO LINK:" in error:
            num_no_link += 1
        elif "NO PAGE:" in error:
            num_no_page += 1
        else:
            num_dis_page += 1
    return num_no_link, num_no_page, num_dis_page


if __name__ == "__main__":
    f = open("./dataset/dataset_paper.json", "r")
    dataset_game = json.load(f)
    f.close()

    # Placeholder for results
    results = []

    # Iterate over all game modes and games
    s = 0
    # Iterate over all game modes and games
    for game_mode, game_list in dataset_game.items():
        # Iterate over all games
        for game_num, game in enumerate(game_list[:num_game_test]):
            # Get the start and end nodes
            start = game["start_node"]
            end = game["end_node"]
            request = f"Start_Node: {start} - End_Node: {end}"
            # Get the average human step to win
            avg_human_step_to_win = game["avg_human_step_to_win"]
            # Initialize the human paths string
            human_paths = ""
            # Get the list of human paths with result
            list_path_user_with_result = game["list_path_user_with_result"]
            # Iterate over all human paths
            for path_user in list_path_user_with_result:
                # If the path is correct, we add it to the human paths string
                if path_user[1] == True:
                    # Add the path to the human paths string with the @#@ separator for an human readable format
                    human_paths += path_user[0] +" @#@\n"
            # Iterate over all context types
            for context_type in context_types:
                context = context_type[1]
                for model in list_model: 
                    # If the context type is not LINK, we use the normal context
                    if context_type[0] != "LINK":
                        if model[0] == "GPT":
                            steps = call_gpt(context, request, model[1])
                        elif model[0] == "LLAMA":
                            steps = call_llama(context, request)
                    # If the context type is LINK, we use the link context
                    else:
                        # Initialize the steps list with the start node
                        steps = [start]
                        # Create the request for the link context
                        request_link = f"Start_Node: {start} - End_Node: {end}\n\nList_Link_From_Start_Node:\n{str(get_all_visible_existing_internal_links(start, steps))}"
                        # Call the model to get the next step
                        if model[0] == "GPT":
                            new_step = call_gpt_link(context, request_link, model[1])
                        elif model[0] == "LLAMA":
                            new_step = call_llama_link(context, request_link)
                        steps.append(new_step)
                        # While the last step is not the end node and the number of steps is less than the maximum number of steps, we call the model to get the next step
                        while steps[-1].lower() != end.lower() and len(steps) < max_steps_try:
                            # Create the request for the link context
                            request_link = f"Start_Node: {new_step} - End_Node: {end}\n\nList_Link_From_Start_Node:\n{str(get_all_visible_existing_internal_links(new_step, steps))}"
                            # Call the model to get the next step
                            if model[0] == "GPT":
                                new_step = call_gpt_link(context, request_link, model[1])
                            elif model[0] == "LLAMA":
                                new_step = call_llama_link(context, request_link)
                            steps.append(new_step)
                    # Try to check the errors in the steps
                    try:
                        # Check the errors in the steps
                        errors = check_error_steps(steps)
                        # Count the number of errors
                        num_no_link, num_no_page, num_dis_page = count_error_steps(errors)
                    # If there is an error, we set the errors to NO CORRECT PATH
                    except:
                        errors = ["NO CORRECT PATH"]
                        num_no_link=0
                        num_no_page=0
                        num_dis_page=0
                    # Check if the path is complete
                    complete_path = "True" if end in steps else "False"
                    # Append the results to the list
                    results.append({
                        "game_mode": game_mode,
                        "game_num": game_num,
                        "model_name": model[0],
                        "version_model": model[1],
                        "type_context": context_type[0],
                        "inference_mode": "UNSUPERVISED",
                        "start_node": start,
                        "end_node": end,
                        "steps": " ->\n".join(steps),
                        "errors": errors,
                        "num_no_link": num_no_link,
                        "num_no_page": num_no_page,
                        "num_dis_page": num_dis_page,
                        "complete_path": complete_path,
                        "avg_human_step_to_win": avg_human_step_to_win,
                        "human_paths": human_paths
                    })

    # Create DataFrame and save in Excel
    df = pd.DataFrame(results)
    df.to_excel("./results/results_wikigame.xlsx", index=False)


