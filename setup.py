from setuptools import find_packages,setup

setup(
    name = 'mcqgenerator',
    version = '0.0.1',
    author = 'raghava',
    author_email = 'raghava000@gmail.com',
    install_requires = ["openai","langchain", "streamlit","pythion-dotenv", "PyPDF2"],
    packages=find_packages()
)