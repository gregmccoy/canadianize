from distutils.core import setup

setup(
        name = 'Canadianize',
        author = "Greg McCoy",
        author_email = "gregmccoy@gfa.org",
        url = "https://github.com/gregmccoy/canadianize",
        version = '0.3.1',
        license='MIT',
        long_description=open('README.md').read(),
        requires = [
            'enchant',
            'html2text',
            'pytz',
        ],
        packages=['fix_emails'],
    )
