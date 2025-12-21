import subprocess
import argparse

#versions = ['v0.12.1','v0.12.2','v0.12.3','v0.12.4','v0.12.5']
#versions = ['v0.14.2','v0.14.1','v0.14.0','dev']
#versions = ['v0.14.16']

description = """Create Dockerfiles for DBMSBenchmarker images in bexhoma - benchmarker"""

parser = argparse.ArgumentParser(description=description)
parser.add_argument('-v', '--version', help='which version of DBMSBenchmarker to use', default='v0.14.16')
parser.add_argument('-i', '--image-tag', help='tag of the image to be created', default='v0.14.16')
args = parser.parse_args()

versions = [args.version]
image_versions = [args.image_tag]

with open('Dockerfile_template', 'r') as file:
	dockerfile = file.read()

print(dockerfile)

for version in versions:
	print(version)
	filename_versioned = 'Dockerfile_{}'.format(version)
	with open(filename_versioned, 'w') as file:
		file.write(dockerfile.format(version=version, DBMSBENCHMARKER_CONNECTION="{DBMSBENCHMARKER_CONNECTION}"))
	#subprocess.call(['docker', 'build', '-f', filename_versioned, '--no-cache', '-t', 'bexhoma/benchmarker_dbmsbenchmarker:'+args.image_tag, '.'])
	subprocess.call(['docker', 'build', '-f', filename_versioned, '-t', 'bexhoma/benchmarker_dbmsbenchmarker:'+args.image_tag, '.'])
