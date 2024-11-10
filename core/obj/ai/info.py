

from core.obj.ai.common import f_ai_ai

def f_ai_models(inter, line, args, **kwargs):
    return f_ai_ai(inter, line, args, **kwargs)


def f_ai_max_tokens(inter, line, args, **kwargs):
    # prepare
    models = f_ai_ai(inter, line, args, **kwargs)
    # get model
    model = inter.parse(0, line, args)[2]
    # check model
    models["check_model"](model)
    # return max tokens
    return models[model]["max_tokens"]


def f_ai_price_per_token(inter, line, args, **kwargs):
    # prepare
    models = f_ai_ai(inter, line, args, **kwargs)
    # get the model
    model = inter.parse(0, line, args)[2]
    # check the model
    models["check_model"](model)
    # return price per token
    return models[model]["price_per_token"]

def f_ai_tokens(inter, line, args, **kwargs):
    import tiktoken
    models = f_ai_ai(inter, line, args, **kwargs)
    # string to check
    prompt = inter.parse(0, line, args)[2]
    # prompt must be str
    inter.type_err([(prompt, (str,))], line, kwargs["lines_ran"])
    # model to check
    model_name = inter.parse(1, line, args)[2]
    # check model
    models["check_model"](model_name)
    # get the encoding
    return len(
        tiktoken.encoding_for_model(model_name).encode(prompt)
    )



OBJ_AI_INFO_DISPATCH = {
    "models": f_ai_models,
    "max_tokens": f_ai_max_tokens,
    "price_per_token": f_ai_price_per_token,
    "tokens": f_ai_tokens,
}