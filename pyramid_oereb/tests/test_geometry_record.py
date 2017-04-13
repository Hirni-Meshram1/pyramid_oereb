# -*- coding: utf-8 -*-

import datetime
import pytest
from shapely.geometry import Point

from pyramid_oereb.lib.records.geometry import GeometryRecord
from pyramid_oereb.lib.records.office import OfficeRecord


def test_get_fields():
    expected_fields = [
        'legal_state',
        'published_from',
        'geo_metadata',
        'geom',
        'public_law_restriction',
        'office'
    ]
    fields = GeometryRecord.get_fields()
    assert fields == expected_fields


def test_mandatory_fields():
    with pytest.raises(TypeError):
        GeometryRecord()


def test_init():
    record = GeometryRecord('runningModifications', datetime.date(1985, 8, 29), 'test')
    assert isinstance(record.legal_state, str)
    assert isinstance(record.published_from, datetime.date)
    assert isinstance(record.geo_metadata, str)
    assert record.geom is None
    assert record.public_law_restriction is None
    assert record.office is None


def test_to_extract():
    office = OfficeRecord('Office')
    record = GeometryRecord('runningModifications', datetime.date(1985, 8, 29), 'test',
                            geom=Point((0, 0)), office=office)
    assert record.to_extract() == {
        'legal_state': 'runningModifications',
        'geo_metadata': 'test',
        'geom': Point((0, 0)),
        'office': {
            'name': 'Office'
        }
    }
