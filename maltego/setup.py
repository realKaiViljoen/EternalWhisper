from setuptools import setup, find_packages

setup(
    name='eternalwhisper-maltego',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'maltego-trx>=1.7.0',
    ],
    entry_points={
        'maltego_trx.transforms': [
            'eternalwhisper = maltego.transforms:registry'
        ]
    }
)
