# -*- coding: utf-8 -*-

from denite import util
from .base import Base

import os
import site

# Add external modules
path_to_parent_dir = os.path.abspath(os.path.dirname(__file__) + '/../')
path_to_modules = os.path.join(path_to_parent_dir, 'modules')
site.addsitedir(path_to_modules)
site.addsitedir(os.path.join(path_to_modules, 'inflection'))
site.addsitedir(os.path.join(path_to_modules, 'finders'))
site.addsitedir(os.path.join(path_to_modules, 'models'))

from dwim_finder import DwimFinder # noqa
from model_finder import ModelFinder # noqa
from controller_finder import ControllerFinder # noqa
from helper_finder import HelperFinder # noqa
from view_finder import ViewFinder # noqa
from test_finder import TestFinder # noqa
from spec_finder import SpecFinder # noqa
from command_finder import CommandFinder # noqa
from decorator_finder import DecoratorFinder # noqa
from job_finder import JobFinder # noqa
from mailer_finder import MailerFinder # noqa
from presenter_finder import PresenterFinder # noqa
from serializer_finder import SerializerFinder # noqa


class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'rails'
        self.kind = 'file'

    def on_init(self, context):
        try:
            context['__target'] = context['args'][0]
        except IndexError:
            raise NameError('target must be provided')

        cbname = self.vim.current.buffer.name
        context['__cbname'] = cbname
        context['__root_path'] = util.path2project(self.vim, cbname, context.get('root_markers', ''))

    def highlight(self):
        # TODO syntax does not work as expected
        self.vim.command('syntax region deniteSource_railsConstant start=+^+ end=+^.\{-}\s+')
        self.vim.command('highlight link deniteSource_railsConstant Statement')
        self.vim.command('syntax match deniteSource_railsSeparator /::/ containedin=deniteSource_railsConstant')
        self.vim.command('highlight link deniteSource_railsSeparator Identifier')
        self.vim.command('syntax region deniteSource_railsPath start=+(+ end=+)+')
        self.vim.command('highlight link deniteSource_railsPath Statement')
        self.vim.command('syntax match deniteSource_railsController /Controller:/')
        self.vim.command('highlight link deniteSource_railsController Function')
        self.vim.command('syntax match deniteSource_railsModel /Model:/')
        self.vim.command('highlight link deniteSource_railsModel String')
        self.vim.command('syntax match deniteSource_railsHelper /Helper:/')
        self.vim.command('highlight link deniteSource_railsHelper Type')
        self.vim.command('syntax match deniteSource_railsView /View:/')
        self.vim.command('highlight link deniteSource_railsView Statement')
        self.vim.command('syntax match deniteSource_railsTest /Test:/')
        self.vim.command('highlight link deniteSource_railsTest Number')
        self.vim.command('syntax match deniteSource_railsSpec /Spec:/')
        self.vim.command('highlight link deniteSource_railsSpec Number')
        self.vim.command('syntax match deniteSource_railsCommand /Command:/')
        self.vim.command('highlight link deniteSource_railsCommand String')
        self.vim.command('syntax match deniteSource_railsDecorator /Decorator:/')
        self.vim.command('highlight link deniteSource_railsDecorator String')
        self.vim.command('syntax match deniteSource_railsJob /Job:/')
        self.vim.command('highlight link deniteSource_railsJob String')
        self.vim.command('syntax match deniteSource_railsMailer /Mailer:/')
        self.vim.command('highlight link deniteSource_railsMailer String')
        self.vim.command('syntax match deniteSource_railsPresenter /Presenter:/')
        self.vim.command('highlight link deniteSource_railsPresenter String')
        self.vim.command('syntax match deniteSource_railsSerializer /Serializer:/')
        self.vim.command('highlight link deniteSource_railsSerializer String')


    def gather_candidates(self, context):
        file_list = self._find_files(context)
        if file_list is not None:
            return [self._convert(context, x) for x in file_list]
        else:
            return []

    def _find_files(self, context):
        target = context['__target']

        if target == 'dwim':
            finder_class = DwimFinder
        elif target == 'model':
            finder_class = ModelFinder
        elif target == 'command':
            finder_class = CommandFinder
        elif target == 'job':
            finder_class = JobFinder
        elif target == 'mailer':
            finder_class = MailerFinder
        elif target == 'decorator':
            finder_class = DecoratorFinder
        elif target == 'controller':
            finder_class = ControllerFinder
        elif target == 'helper':
            finder_class = HelperFinder
        elif target == 'presenter':
            finder_class = PresenterFinder
        elif target == 'serializer':
            finder_class = SerializerFinder
        elif target == 'view':
            finder_class = ViewFinder
        elif target == 'test':
            finder_class = TestFinder
        elif target == 'spec':
            finder_class = SpecFinder
        else:
            msg = '{0} is not valid denite-rails target'.format(target)
            raise NameError(msg)

        return finder_class(context).find_files()

    def _convert(self, context, file_object):
        result_dict = {
            'word': file_object.to_word(context['__root_path']),
            'action__path': file_object.filepath
        }

        return result_dict
