from setuptools import setup, find_packages

setup(
    name='ruia_ocr',
    version='1.0.1',
    author='fffoobibi',
    author_email='1564002691@qq.com',
    description='simple ruia ocr-plugin',
    long_description='',
    license='MIT',
    url=r'https://github.com/fffoobibi/ruia_ocr',
    packages=find_packages(),
    install_requires=['baidu_aip>=2.2.17', 'ruia>=0.6.2'],
    requires=['baidu_aip', 'ruia'],
    classifiers=['Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9']
)
