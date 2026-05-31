from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pyfileshare',
    version='1.0.0',
    author='a-t-better',
    author_email='',
    description='一个高性能、可配置的 Python 内网文件传输工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/a-t-better/py-file-share',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Communications :: File Sharing',
    ],
    python_requires='>=3.8',
    install_requires=[
        'flask>=2.3.0',
        'requests>=2.31.0',
        'pydantic>=2.0',
        'PyYAML>=6.0',
        'cryptography>=41.0',
        'click>=8.1',
        'rich>=13.0',
        'aiohttp>=3.9.0',
        'aiofiles>=23.0',
    ],
    entry_points={
        'console_scripts': [
            'pyfileshare=pyfileshare.cli:main',
        ],
    },
    include_package_data=True,
)
