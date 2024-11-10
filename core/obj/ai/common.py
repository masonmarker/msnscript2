
def f_ai_ai(inter, line, args, **kwargs):
    import os
    import openai
    import tiktoken

    global models
    # verify existence of openai api key
    if not openai.api_key:
        try:
            openai.api_key = os.environ["OPENAI_API_KEY"]
        except:
            # msn2 error, no OPENAI env var
            inter.err(
                f"OpenAI API key not found. Please set your OPENAI_API_KEY environment variable to your OpenAI API key.",
                True,
                "",
                kwargs["lines_ran"],
            )
    # if models not defined, define them
    if not models:
        # determines if a model needs chatcompletion
        def needs_completion(model):
            return (
                model.startswith("text")
                or model == "gpt-3.5-turbo-instruct"
            )

        # determines if arguments for 'model' are str and in models
        def check_model(model):
            # model must be str
            inter.type_err([(model, (str,))], line, kwargs["lines_ran"])
            # model must exist
            if model not in models:
                inter.err(
                    "Model not found",
                    f'Model {model} not found. Available models are {", ".join(models.keys())}',
                    line,
                    kwargs["lines_ran"],
                )
        # gets responses from the models

        def response(model, prompt):
            # enforce model as str and prompt as str
            inter.type_err(
                [(model, (str,)), (prompt, (str,))], line, kwargs["lines_ran"]
            )
            if needs_completion(model):
                # return v1/completions endpoint
                return (
                    openai.Completion.create(
                        model=model,
                        prompt=prompt,
                        temperature=0.5,
                        max_tokens=models[model]["max_tokens"] // 2,
                    )
                    .choices[0]
                    .text
                )
            else:
                return openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=models[model]["max_tokens"] // 2,
                )
        # available models for use by the query
        return {
            "gpt-3.5-turbo-instruct": {
                "max_tokens": 4097,
                # compute $0.0015 / 1K tokens
                "price_per_token": 0.0015 / 1000,
            },
            "gpt-3.5-turbo": {
                "max_tokens": 4097,
                "price_per_token": 0.0015 / 1000,
            },
            "gpt-3.5-turbo-16k": {
                "max_tokens": 16384,
                "price_per_token": 0.003 / 1000,
            },
            "text-davinci-003": {
                "max_tokens": 4097,
                # turbo * 10, as stated by OPENAI model pricing documentation
                "price_per_token": (0.0015 / 1000) * 10,
            },
            # gets responses from these models
            "response": response,
            "needs_completion": needs_completion,
            "check_model": check_model,
        }

    return "<msnint2 class>"