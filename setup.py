from distutils.core import setup

setup(
	name='ipaddr',
	version='0.1',
	author='Jason Carnevale',
	author_email='jason@bean-networks.org',
	packages=['ipaddr', 'ipaddr.test'],
	scripts=[''],
	#url='http://pypi.python.org/pypi/TowelStuff/',
	license='LICENSE.txt',
	description='IPv4 Network/Subnet and Address Manipulation Library',
	long_description=open('README.txt').read(),
	install_requires=[
	],
)
