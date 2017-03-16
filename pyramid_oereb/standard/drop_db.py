# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2016, GIS-Fachstelle des Amtes für Geoinformation des Kantons Basel-Landschaft
# All rights reserved.
#
# This program is free software and completes the GeoMapFish License for the geoview.bl.ch specific
# parts of the code. You can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
import argparse
from pyramid_oereb.standard import drop_tables

__author__ = 'Clemens Rudert'
__create_date__ = '15.03.17'

parser = argparse.ArgumentParser(description='Create all content for the standard database')
parser.add_argument(
    '-d',
    '--database',
    help='The connection string which leads to the desired database',
    required=False
)
args = parser.parse_args()

if args.database:
    drop_tables(connection_string=args.database)
else:
    drop_tables()