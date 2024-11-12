"""Container class, for working with a runnable container."""

import os
import shutil
import uuid
import jsonschema
import subprocess

from core.utils.file import create_temp_dir

correct_mountable_schema = {
    "type": "object",
    "properties": {
        "file": {"type": "string"},
        "body": {"type": "string"},
    },
    "required": ["file", "body"],
    "additionalProperties": False,
}


class Container:
    """A container is a runnable environment for a task."""

    def __init__(self, inter, image, commands=[], mounting=[], name=None, _kwargs={}, **kwargs):
        self.image = image
        self.commands = commands

        # name cannot have
        self.name = name
        self.mounting = mounting
        self.kwargs = kwargs
        self._kwargs = _kwargs
        self.inter = inter

        # generate an id
        self.id = uuid.uuid4().hex

        self.started = False

    def run(self):
        """Run the container."""

        try:
            self.started = True
            self.inter.styled_print([
                {'text': f'[{self.name}] running container...',
                    'fore': 'green'},
            ])
            temp_dir = create_temp_dir()
            self.container_dir = temp_dir
            self.app_dir = self.container_dir + "/root"
            self.full_dir = os.path.join(self.app_dir)
            # create the working root directory
            os.makedirs(self.app_dir)
            # mount the files
            self._mount_files(self.mounting)
            # where the internal process needs to cd to
            # create a process that navigates to the container directory and runs the commands
            try:
                subprocess.run(self.commands, cwd=self.full_dir,
                               shell=True, check=True)
            except Exception as e:
                self.inter.err(
                    "Container error",
                    f"Error running container commands\n{e}",
                    self._kwargs["line"],
                    self._kwargs["lines_ran"],
                )

        except Exception as e:
            self.inter.err(
                "Container error",
                f"Error running container\n{e}",
                self._kwargs["line"],
                self._kwargs["lines_ran"],
            )
        finally:
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
            {'text': f'[{self.name}] cleaning up container...',
                'fore': 'cyan'},
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
            with open(f"{self.app_dir}/{mount['file']}", "w") as file:
                file.write(mount['body'])
