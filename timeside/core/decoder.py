#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2007-2013 Parisson
# Copyright (c) 2007 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2007-2013 Guillaume Pellerin <pellerin@parisson.com>
# Copyright (c) 2010-2013 Paul Brossier <piem@piem.org>
#
# This file is part of TimeSide.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Authors:
# Paul Brossier <piem@piem.org>
# Guillaume Pellerin <yomguy@parisson.com>
# Thomas Fillon <thomas@parisson.com>

from __future__ import division

from timeside.core import Processor, implements, interfacedoc, abstract
from timeside.core.api import IDecoder

from django.conf import settings


class Decoder(Processor):

    """General abstract base class for Decoder
    """
    implements(IDecoder)
    abstract()

    type = 'decoder'

    mimetype = ''
    output_samplerate = None
    output_channels = None

    def __init__(self, start=0, duration=None, progress_callback=None,
                 sample_cursor=None):
        super(Decoder, self).__init__()

        self.uri = ""
        self.uri_start = float(start)
        if duration:
            self.uri_duration = float(duration)
        else:
            self.uri_duration = duration

        if start == 0 and duration is None:
            self.is_segment = False
        else:
            self.is_segment = True
        if progress_callback:
            self.progress_callback = progress_callback
        else:
            self.progress_callback = None
        if sample_cursor:
            self.sample_cursor = sample_cursor
        else:
            self.sample_cursor = 0
        self._sha1 = ""
        self.input_samplerate = 44100
        self.input_channels = 1
        self.input_totalframes = 1

    @interfacedoc
    def channels(self):
        return self.output_channels

    @interfacedoc
    def samplerate(self):
        return self.output_samplerate

    @interfacedoc
    def blocksize(self):
        return self.output_blocksize

    @interfacedoc
    def totalframes(self):
        return self.input_totalframes

    @interfacedoc
    def release(self):
        pass

    @interfacedoc
    def mediainfo(self):
        return dict(uri=self.uri,
                    duration=self.uri_duration,
                    start=self.uri_start,
                    is_segment=self.is_segment,
                    samplerate=self.input_samplerate,
                    sha1=self.sha1)

    @property
    def sha1(self):
        return self._sha1

    def __del__(self):
        self.release()

    @interfacedoc
    def encoding(self):
        return self.format().split('/')[-1]

    @interfacedoc
    def resolution(self):
        return self.input_width

    def process(
        self,
        frames,
        eod,
    ):
        if self.sample_cursor is not None:
            self.sample_cursor += self.blocksize()
            if self.progress_callback and (
                        self.sample_cursor // self.blocksize() %
                        settings.COMPLETION_INTERVAL == 0
                    ):
                self.progress_callback(
                    self.sample_cursor / self.totalframes()
                )

        super(Decoder, self).process(frames, eod)
