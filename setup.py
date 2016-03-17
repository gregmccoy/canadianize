from setuptools import setup

setup(
        name = 'versebg',
        author = "Greg McCoy",
        author_email = "gregmccoy@gfa.org",
        url = "",
        version = '0.2.1',
        packages=['ca'],
        package_dir={'ca': 'src/ca'},
        package_data={'ca': 'data/*'},
        scripts=['ca'],
        license='MIT',
        long_description=open('README.md').read(),

        install_requires = ['enchant', 'html2text']
    )
