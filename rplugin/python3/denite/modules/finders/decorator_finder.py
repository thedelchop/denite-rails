import finder_utils

from decorator_file import DecoratorFile


class DecoratorFinder:

    GLOB_PATTERN = 'app/decorators/**/*.rb'

    def __init__(self, context):
        self.context = context
        self.root_path = context['__root_path']

    def find_files(self):
        files = finder_utils.glob_project(self.root_path, self.GLOB_PATTERN)
        return [DecoratorFile(filename) for filename in files]
