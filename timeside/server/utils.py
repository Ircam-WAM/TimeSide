# -*- coding: utf-8 -*-
import os

import timeside.core
import json
from timeside.core.api import IEncoder
from timeside.server.models import Processor, Preset, Result, Task

TS_ENCODERS = timeside.core.processor.processors(IEncoder)
TS_ENCODERS_EXT = {encoder.file_extension(): encoder.id()
                   for encoder in TS_ENCODERS
                   if encoder.file_extension()}


def get_or_run_proc_result(pid, item, parameters='{}'):

    # Get or Create Processor
    processor, c = Processor.objects.get_or_create(pid=pid)

    if not parameters:
        parameters = processor.get_parameters_default()

    # Get or Create Preset with Processor
    preset, c = Preset.get_first_or_create(
        processor=processor,
        parameters=parameters
        )

    return get_result(item, preset, wait=True)

# TODO def get_or_run_proc_item(pid, version, item, prarameters={}):
# don't run the task if results exist for a proc with its version


def get_result(item, preset, wait=True):
    # Get or create Result with preset and item
    result, created = Result.get_first_or_create(
        preset=preset,
        item=item
        )
    if created or not result.has_file() and not result.has_hdf5():
        task, c = Task.get_first_or_create(
            experience=preset.get_single_experience(),
            item=item
            )
        task.run(wait=wait)
        # SMELLS: might not get the last good result
        # TODO: manage Task running return for Analysis through API
        result, created = Result.get_first_or_create(
            preset=preset,
            item=item
            )
        return result

    else:
        return result
