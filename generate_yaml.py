import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

konnect_service_name = os.environ.get('KONNECT_SERVICE_NAME')
konnect_runtime_group = os.environ.get('KONNECT_RUNTIME_GROUP')

if not os.path.exists('results'):
    os.makedirs('results')

file_name = os.getcwd() + '/kong/{0}/{1}_{2}.yaml'.format(konnect_runtime_group,konnect_service_name, konnect_runtime_group)
results_file_name = os.getcwd() + '/results/{0}_{1}.yaml'.format(konnect_service_name, konnect_runtime_group)
print("Results file is :" + results_file_name)

try:
    with open(file_name, 'r') as file:
        values = yaml.safe_load(file)
        # Load templates file from templates folder
        env = Environment(loader = FileSystemLoader('./templates'),   trim_blocks=True, lstrip_blocks=True)
        
        template = env.get_template('{0}.yaml.j2'.format(konnect_service_name))
        file=open(results_file_name, "w")
        file.write(template.render(values))
        file.close()
except TemplateNotFound as e:
    sys.exit('Template might not be found, ensure your template file exists in templates folder of repo with name being just the service name and does not have environment : {}'.format(e))
except FileNotFoundError as e:
    sys.exit('Error loading results file - ensure service specific values file with name being servicename underscore environment name exists in repo and also verify if correct service name is passed from pipeline : {}'.format(e))

print("Yaml file is generated successfully")

try:
    with open(results_file_name) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print(data)
        f.close()
except Exception as e:
    sys.exit('Error processing template file: {}'.format(e))