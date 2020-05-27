
from django.contrib import admin
from timeside.server.models import *


class PresetAdmin(admin.ModelAdmin):
    model = Preset
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'processor', 'parameters', 'date_added', 'date_modified']
    list_filter = ['date_modified', 'processor']
    search_fields = ['uuid', 'processor__name']


class ProcessorAdmin(admin.ModelAdmin):
    model = Processor
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'pid']
    search_fields = ['uuid', 'name']


class SelectionAdmin(admin.ModelAdmin):
    model = Selection
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified']
    list_filter = ['date_modified']
    filter_horizontal = ['items', 'selections']
    search_fields = ['title', 'uuid']


class ExperienceAdmin(admin.ModelAdmin):
    model = Experience
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified']
    list_filter = ['date_modified', 'title']
    filter_horizontal = ['presets', 'experiences']
    search_fields = ['uuid', 'title']


class TaskAdmin(admin.ModelAdmin):
    model = Task
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified', 'status']
    list_filter = ['date_modified', 'status']
    search_fields = ['uuid']


class ResultAdmin(admin.ModelAdmin):
    model = Result
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'run_time', 'mime_type', 'status', 'date_added', 'date_modified', 'uuid']
    list_filter = ['date_modified', 'status', 'item', 'preset']
    search_fields = ['uuid']


class AnalysisAdmin(admin.ModelAdmin):
    model = Analysis
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified', 'render_type']
    list_filter = ['date_modified', 'uuid']


class AnalysisTrackAdmin(admin.ModelAdmin):
    model = AnalysisTrack
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified']
    list_filter = ['date_modified']
    search_fields = ['uuid', 'title']


class ProviderAdmin(admin.ModelAdmin):
    model = Provider
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid']
    search_fields = ['uuid', 'name']
    
class ItemAdmin(admin.ModelAdmin):
    model = Item
    readonly_fields = ('uuid',)
    list_display = ['__str__', 'uuid', 'date_added', 'date_modified']
    search_fields = ['uuid', 'title']

admin.site.register(Selection, SelectionAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Processor, ProcessorAdmin)
admin.site.register(SubProcessor)

admin.site.register(Preset, PresetAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Analysis, AnalysisAdmin)
admin.site.register(AnalysisTrack, AnalysisTrackAdmin)
admin.site.register(Annotation)
admin.site.register(AnnotationTrack)

admin.site.register(Provider, ProviderAdmin)
