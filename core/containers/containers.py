"""Functions for creating and working with containers."""
"""UNFINISHED"""

import jsonschema
from jsonschema import validate

from core.classes.containers.container import Container

correct_schema = {
    "type": "object",
    "properties": {
        "image": {"type": "object"},
        "commands": {"type": "array"},
        "mounting": {"type": "array"},
        "name": {"type": "string"},
    },
    "required": ["image"],
    "additionalProperties": False,
}

correct_image_schema = {
    "type": "object",
    "properties": {
        "requirements": {"type": "array"},
    },
    "required": ["requirements"],
    "additionalProperties": False,
}
# should be an array of objects
correct_mounting_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "extension": {"type": "string"},
            "body": {"type": "string"},
        },
        "required": ["extension", "body"],
        "additionalProperties": False,
    },
    "additionalItems": False,
}

def _verify_container_image(image_config):
    print(image_config)
    try:
        validate(instance=image_config, schema=correct_image_schema)
    except jsonschema.ValidationError as e:
        return f"Invalid image configuration\n{e}"
    return image_config

def _verify_container_mounting(mounting_config):
    try:
        validate(instance=mounting_config, schema=correct_mounting_schema)
    except jsonschema.ValidationError as e:
        return f"Invalid mounting configuration\n{e}"
    return mounting_config

# verifies the container()'s configuration is correct
def _verify_container_config(inter, line, args, **kwargs):
    from pprint import pprint
    config = inter.parse(0, line, args)[2]
    # config should be a dictionary
    inter.type_err([(config, (dict,))], line, kwargs["lines_ran"])    
    # verify the config is correct
    try:
        jsonschema.validate(config, correct_schema)
    except jsonschema.ValidationError as e:
        return inter.err(
            "Container error",
            f"Invalid container configuration\n{e}",
            line,
            kwargs["lines_ran"],
        )
    # verify the image is correct
    # get the image from the config
    image_config = config.get("image", {})
    # verify the image is correct
    image_config = _verify_container_image(image_config)
    # verify the mounting is correct
    mounting_config = config.get("mounting", [])
    mounting_config = _verify_container_mounting(mounting_config)
    return config

def f_container(inter, line, args, **kwargs):
    config = _verify_container_config(inter, line, args, **kwargs)
    """Create a container."""
    return Container(**config)



CONTAINERS_DISPATCH = {
    "container": f_container,
}