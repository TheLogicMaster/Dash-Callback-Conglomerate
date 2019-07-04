from distutils.core import setup

setup(
    name='DashCallbackConglomerate',
    version='0.1.0',
    author='Justin Marentette',
    author_email='justinmarentette11@gmail.com',
    packages=['dash_callback_conglomerate'],
    url='https://github.com/TheLogicMaster/Dash-Callback-Conglomerate',
    license='LICENSE.txt',
    description='Enable duplicated inputs and outputs, and without changing a single callback.',
    long_description=open('README.md').read(),
    install_requires=[
        "Dash >= 0.38.0"
    ],
)