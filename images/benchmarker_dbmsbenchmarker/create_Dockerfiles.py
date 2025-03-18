import subprocess

#versions = ['v0.12.1','v0.12.2','v0.12.3','v0.12.4','v0.12.5']
#versions = ['v0.14.2','v0.14.1','v0.14.0','dev']
versions = ['v0.14.7']

with open('Dockerfile_template', 'r') as file:
	dockerfile = file.read()

print(dockerfile)

for version in versions:
	print(version)
	filename_versioned = 'Dockerfile_{}'.format(version)
	with open(filename_versioned, 'w') as file:
		file.write(dockerfile.format(version=version, DBMSBENCHMARKER_CONNECTION="{DBMSBENCHMARKER_CONNECTION}"))
	subprocess.call(['docker', 'build', '-f', filename_versioned, '-t', 'bexhoma/benchmarker_dbmsbenchmarker:'+version, '.'])
