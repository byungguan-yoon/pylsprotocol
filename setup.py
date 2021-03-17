from setuptools import setup, find_packages


setup(
    name             = 'pylsprotocol',
    version          = '0.1',
    description      = 'LS protocol enables you to operate PLC from computer.',
    long_description = open('README.md').read(),
    author           = 'byungguan.yoon',
    author_email     = 'bkaunyun@naver.com',
    url              = 'https://github.com/byungguan-yoon/pylsprotocol',
    download_url     = 'https://github.com/byungguan-yoon/pylsprotocol/archive/main.zip',
    install_requires = [''],
    packages         = find_packages(exclude = ['docs', 'example']),
    keywords         = ['PLC', 'protocol', 'LS electric'],
    python_requires  = '>=3',
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)