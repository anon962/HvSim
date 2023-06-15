from mako.template import Template
from mako import exceptions
import ruamel.yaml, sys

def render(template, dct):
	try:
		dct= { x.upper():y for x,y in dct.items() }
		return Template(template).render(**dct)
	except:
		print(exceptions.text_error_template().render(), file=sys.stderr)

def load_yaml(file_path):
	txt= open(file_path).read()
	return ruamel.yaml.load(txt, ruamel.yaml.Loader)

def dump_yaml(data, file_path):
	with open(file_path, "w+") as f:
		ruamel.yaml.dump(data)
