from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fogis-session-tools",
    version="0.1.0",
    author="PitchConnect",
    author_email="info@pitchconnect.io",
    description="Tools for managing persistent sessions with the Fogis API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PitchConnect/fogis-session-tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fogis-api-client-timmybird",
        "python-dotenv",
        "requests",
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "black",
        ],
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "fogis-tools=fogis_session_tools.fogis_tools:main",
            "fogis-session-keeper=fogis_session_tools.fogis_session_keeper:main",
            "fogis-save-cookies=fogis_session_tools.save_fogis_cookies:main",
            "fogis-check-status=fogis_session_tools.check_session_status:main",
        ],
    },
)
