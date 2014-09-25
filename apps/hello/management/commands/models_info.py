from django.core.management.base import BaseCommand
import inspect
import os
from django.conf import settings
from imp import load_source
from django.db import connection


class Command(BaseCommand):
    help = 'Prints all project models and the count of objects in every model'

    def handle(self, *args, **options):
        module_name_to_path_map = {}
        module_name_to_app_name = {}
        apps_path = os.path.join(settings.BASE_DIR, 'apps')
        for app_name in os.listdir(apps_path):
            if os.path.isdir(os.path.join(apps_path, app_name)):
                for module_name in os.listdir(os.path.join(apps_path, app_name)):
                    if os.path.isfile(os.path.join(apps_path, app_name, module_name)):
                        if module_name == 'models.py':
                            module_name_to_path_map['apps.%s.%s' % (app_name, 'models')] = \
                                os.path.join(apps_path, app_name, 'models.py')
                            module_name_to_app_name['apps.%s.%s' % (app_name, 'models')] = app_name

        cursor = connection.cursor()
        table_names = connection.introspection.get_table_list(cursor)

        for module_name in module_name_to_path_map:
            try:
                module = load_source(module_name, module_name_to_path_map[module_name])
                for name, data in inspect.getmembers(module, inspect.isclass):
                    table_name = module_name_to_app_name[module_name] + '_' + name.lower()
                    if table_name in table_names:
                        objects_count = 0
                        try:
                            model_objects = data.objects.all()
                            objects_count = model_objects.count()
                        except AttributeError:
                            self.stderr.write('error: could not determine model %s' % name)

                        self.stdout.write('Model %s: objects: %d' % (name, objects_count))
                        self.stderr.write('error: model %s: objects: %d' % (name, objects_count))
            except ImportError:
                pass
