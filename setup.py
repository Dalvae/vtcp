from setuptools import setup, find_packages

setup(
    name="vtcp",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,  
    package_data={
        'vtcp': ['assets/*.wav'],  
    },
    install_requires=[
        'azure-cognitiveservices-speech',
        'pyperclip',
        'numpy',
        'sounddevice',
        'python-dotenv',
        'rich', 
        'simpleaudio'
    ],
    entry_points={
        'console_scripts': [
            'vtcp=vtcp.main:main',
        ],
    },
    author="Diego Alvarez",
    description="Voice to clipboard utility",
    python_requires=">=3.7",
)