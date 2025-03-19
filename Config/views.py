from django.shortcuts import render
from django.http import JsonResponse
import configparser
from API.configfile import configFile
import json


class Config:

    def __init__(self):
        self.configFile = configFile.read_config()

    def readConfig(self, request):
        config_data = {}
        for section, settings in self.configFile.items() :
            config_data[section] = {key: settings[key] for key in settings}
        if request.method == 'POST':
            try:
                updated_content = request.POST.dict()
                configParser = configparser.ConfigParser()
                for section, values in updated_content.items():
                    section_parts = section.split('=', 1)  # Section name is before the first '_'
                    if len(section_parts) > 1 :
                        section_name = section_parts[0]
                        key = section_parts[1]
                        if not configParser.has_section(section_name) :
                            configParser.add_section(section_name)
                        configParser.set(section_name, key, values)
                with open('.\\config.ini', 'w') as configfile :
                    configParser.write(configfile)
                return render(request, 'Config.html', {'config_data': configParser, "message" : "Config save successful"})
            except Exception as e:
                return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
        else:
            return render(request, 'Config.html', {'config_data': config_data})
