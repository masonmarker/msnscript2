"""Container class, for working with a runnable container."""

import os
import shutil
import uuid
import jsonschema

from core.utils.file import create_temp_dir

correct_mountable_schema = {
    "type": "object",
    "properties": {
        "extension": {"type": "string"},
        "body": {"type": "string"},
    },
    "required": ["extension", "body"],
    "additionalProperties": False,
}


class Container:
    """A container is a runnable environment for a task."""

    def __init__(self, inter, image, commands=[], mounting=[], name=None, **kwargs):
        self.image = image
        self.commands = commands
        
        
        # name cannot have 
        self.name = name
        self.mounting = mounting
        self.kwargs = kwargs
        self.inter = inter

        # generate an id
        self.id = uuid.uuid4().hex

        self.started = False

    def run(self):
        """Run the container."""
        
        self.started = True
        self.inter.styled_print([
            {'text': f'[{self.name}] running container...', 'fore': 'green'},
        ])
        temp_dir = create_temp_dir()
        self.container_dir = temp_dir
        self.app_dir = self.container_dir + "/root"
        # create the working root directory
        os.makedirs(self.app_dir)
        print(self.app_dir, os.path.exists(self.app_dir))
        exit()
        # mount the files
        self._mount_files(self.mounting)
        # where the internal process needs to cd to
        # create a process that navigates to the container directory and runs the commands
        self.inter.interpret(f"""proc('container_{self.name}_{self.id}', console(
            "echo {self.app_dir}",
            "cd {self.app_dir}",
            ls({self.commands[0]}) 
        ))""")
        # clean up the container
        # first, stop the container
        self.stop()
        # remove traces of the container
        self.cleanup()

    def stop(self):
        """Stop the container."""
        self.inter.styled_print([
            {'text': f'[{self.name}] stopping container...', 'fore': 'red'},
        ])

    def logs(self):
        """Get the logs from the container."""
        pass

    def cleanup(self):
        """Cleanup the container. Removes all traces of the container."""
        self.inter.styled_print([
            {'text': f'[{self.name}] cleaning up container...', 'fore': 'cyan'},
        ])
        # clear the container directory
        shutil.rmtree(self.container_dir)

    def _mount_files(self, mounting):
        # for each object, verify we're in the format {'extension': 'string', 'body':'string'}
        # with jsonschema
        for mount in mounting:
            try:
                jsonschema.validate(
                    instance=mount, schema=correct_mountable_schema)
            except jsonschema.ValidationError as e:
                raise ValueError(f"Invalid mounting configuration\n{e}")
            # write the file
            with open(f"{self.app_dir}/{mount['extension']}", "w") as file:
                file.write(mount['body'])
