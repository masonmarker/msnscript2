"""Container class, for working with a runnable container."""

import os
import uuid

from core.utils.file import create_temp_dir




class Container:
    """A container is a runnable environment for a task."""

    def __init__(self, image, commands=[], mounting=[], name=None, **kwargs):
        self.image = image
        self.command = commands
        self.name = name
        self.mounting = mounting
        self.kwargs = kwargs

        # generate an id
        self.id = uuid.uuid4().hex

        self.started = False

    def run(self):
        """Run the container."""
        self.started = True
        temp_dir = create_temp_dir()
        self.container_dir = temp_dir
        self.app_dir = self.container_dir + "/root"
        # create the working root directory
        os.makedirs(self.app_dir)
        
        # clean up the container
        # first, stop the container
        self.stop()
        # remove traces of the container
        self.cleanup()

    def stop(self):
        """Stop the container."""
        pass

    def logs(self):
        """Get the logs from the container."""
        pass

    def cleanup(self):
        """Cleanup the container. Removes all traces of the container."""
        # remove the container directory
        os.removedirs(self.container_dir)
