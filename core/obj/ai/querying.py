
from core.obj.ai.common import f_ai_ai

def f_ai_basic(inter, line, args, **kwargs):
    models = f_ai_ai(inter, line, args, **kwargs)
    
    # prepare ai
    # generates an ai response with the basic model
    return models["response"](
        inter.parse(0, line, args)[2],
        inter.parse(1, line, args)[2],
    )


def f_ai_advanced(inter, line, args, **kwargs):
    models = f_ai_ai(inter, line, args, **kwargs)
    return models["response"](
        "gpt-3.5-turbo-16k", inter.parse(0, line, args)[2]
    )


def f_ai_query(inter, line, args, **kwargs):
    import openai
    models = f_ai_ai(inter, line, args, **kwargs)
    # model to use
    model = inter.parse(0, line, args)[2]
    # check model
    models["check_model"](model)
    # messages
    messages = inter.parse(1, line, args)[2]
    inter.type_err([(messages, (list, str))], line, kwargs["lines_ran"])
    # temperature
    temperature = inter.parse(2, line, args)[2]
    # temp must be int or float
    inter.type_err([(temperature, (int, float))], line, kwargs["lines_ran"])
    # max_tokens
    max_tokens = inter.parse(3, line, args)[2]
    # max_tokens must be int
    inter.type_err([(max_tokens, (int,))], line, kwargs["lines_ran"])
    # top_p
    top_p = inter.parse(4, line, args)[2]
    # top_p must be int or float
    inter.type_err([(top_p, (int, float))], line, kwargs["lines_ran"])
    # frequency_penalty
    frequency_penalty = inter.parse(5, line, args)[2]
    # frequency_penalty must be int or float
    inter.type_err([(frequency_penalty, (int, float))],
                   line, kwargs["lines_ran"])
    # presence_penalty
    presence_penalty = inter.parse(6, line, args)[2]
    # presence_penalty must be int or float
    inter.type_err([(presence_penalty, (int, float))],
                   line, kwargs["lines_ran"])
    # stop
    stop = inter.parse(7, line, args)[2]
    # stop must be str
    inter.type_err([(stop, (str,))], line, kwargs["lines_ran"])
    # if model is standard
    if models["needs_completion"](model):
        return (
            openai.Completion.create(
                model=model,
                prompt=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop,
            )
            .choices[0]
            .text
        )
    else:
        return openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
        )
def f_ai_split_string(inter, line, args, **kwargs):
    # need langchain
    from langchain.text_splitter import TokenTextSplitter
    models = f_ai_ai(inter, line, args, **kwargs)
    # model_name
    model_name = inter.parse(0, line, args)[2]
    # check model
    models["check_model"](model_name)
    # chunk size
    chunk_size = inter.parse(1, line, args)[2]
    # chunk size must be int
    inter.type_err([(chunk_size, (int,))], line, kwargs["lines_ran"])
    # string to split
    string = inter.parse(2, line, args)[2]
    # string must be str
    inter.type_err([(string, (str,))], line, kwargs["lines_ran"])
    # get the splitter, split by sentence
    splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=0,
        model_name=model_name,
    )
    # split the string
    return splitter.split_text(string)


OBJ_AI_QUERYING_DISPATCH = {
    "basic": f_ai_basic,
    "advanced": f_ai_advanced,
    "query": f_ai_query,
    "split_string": f_ai_split_string,
}
