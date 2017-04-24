# -*- coding: utf-8 -*-

import pytest
from sqlalchemy.orm.exc import NoResultFound

from pyramid_oereb.lib.adapter import DatabaseAdapter
from pyramid_oereb.lib.sources.glossary import GlossaryDatabaseSource
from pyramid_oereb.models import PyramidOerebMainGlossary
from pyramid_oereb.tests.conftest import config_reader


@pytest.mark.run(order=2)
def test_init():
    source = GlossaryDatabaseSource(**config_reader.get_glossary_config().get('source').get('params'))
    assert isinstance(source._adapter_, DatabaseAdapter)
    assert source._model_ == PyramidOerebMainGlossary


@pytest.mark.run(order=2)
@pytest.mark.parametrize("param", [
    {'id': 1, 'title': 'PLR Cadastre', 'content': 'Public Law Restriction Cadastre'}
])
def test_read(param):
    source = GlossaryDatabaseSource(**config_reader.get_glossary_config().get('source').get('params'))
    with pytest.raises(NoResultFound):
        source.read(param.get('id'), param.get('title'), param.get('content'))


@pytest.mark.run(order=2)
def test_missing_parameter():
    source = GlossaryDatabaseSource(**config_reader.get_glossary_config().get('source').get('params'))
    with pytest.raises(TypeError):
        source.read()
