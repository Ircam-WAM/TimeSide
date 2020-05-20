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

    # Get or Create Preset with processor
    preset, c = Preset.get_first_or_create(
        processor=processor,
        parameters=parameters
        )

    # Get or create Result with preset and item
    result, created = Result.get_first_or_create(
        preset=preset,
        item=item
        )

    if created or not result.hdf5 or not os.path.exists(
        result.hdf5.path
            ):
        task, c = Task.get_first_or_create(
            experience=preset.get_single_experience(),
            item=item
            )
        task.run(wait=True)
        # SMELLS: might not get the last good result
        result, created = Result.get_first_or_create(
            preset=preset,
            item=item
            )
        return result

    else:
        return result

# TODO def get_or_run_proc_item(pid, version, item, prarameters={}):
# don't run the task if results exist for a proc with its version


# SMELLS: recursive calls should be avoided
# function should be moved to .utils
def get_result(item, preset):
    # Get Result with preset and item
    try:
        result = ts.models.Result.objects.get(item=item, preset=preset)
        if not result.hdf5 or not os.path.exists(result.hdf5.path):
            # Result exists but there is no file (may have been deleted)
            result.delete()
            return get_result(item=item, preset=preset)
        return result
    except ts.models.Result.DoesNotExist:
        # Result does not exist
        # the corresponding task has to be created and run
        task, created = ts.models.Task.objects.get_or_create(
            experience=preset.get_single_experience(),
            item=item
            )
        if created:
            task.run(wait=False)
        elif task.status == _RUNNING:
            return 'Task Running'
        else:
            # Result does not exist but task exist and is done, draft or
            # pending
            task.status = _PENDING
            task.save()
        return 'Task Created and launched'
