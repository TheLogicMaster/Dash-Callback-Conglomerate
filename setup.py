from distutils.core import setup

setup(
    name='dash-callback-conglomerate',
    version='0.2',
    author='Justin Marentette',
    author_email='justinmarentette11@gmail.com',
    packages=['dash_callback_conglomerate'],
    url='https://github.com/TheLogicMaster/Dash-Callback-Conglomerate',
    download_url='https://github.com/TheLogicMaster/Dash-Callback-Conglomerate/archive/v01.zip',
    license='MIT License',
    description='Enable duplicated inputs and outputs, and without changing a single callback',
    long_description_content_type="text/markdown",
    long_description=open('README.txt').read(),
    keywords=['DASH', 'CALLBACK', 'ROUTER'],
    classifiers=['Development Status :: 5 - Production/Stable', 'Intended Audience :: Developers',
                 'Programming Language :: Python'],
    install_requires=[
        "Dash >= 0.38.0"
    ],
)
