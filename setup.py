from setuptools import setup, find_packages

setup(
    name='whisper_subtitles',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'hello=whisper_subtitles.cli:hello',
        ],
    },
)
