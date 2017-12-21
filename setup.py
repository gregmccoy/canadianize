from setuptools import setup

setup(
        name = 'Canadianize',
        author = "Greg McCoy",
        author_email = "gregmccoy@gfa.ca",
        url = "https://github.com/gregmccoy/canadianize",
        version = '0.3.1',
        license='MIT',
        long_description=open('README.md').read(),
        install_requires = [
            'pyenchant',
            'html2text',
            'pytz',
        ],
        packages=['fix_emails'],
    )
