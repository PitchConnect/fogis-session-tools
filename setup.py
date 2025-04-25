from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fogis-session-tools",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Tools for managing persistent sessions with the Fogis API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/fogis-session-tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "fogis-api-client-timmybird",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "fogis-tools=fogis_session_tools.fogis_tools:main",
            "fogis-session-keeper=fogis_session_tools.fogis_session_keeper:main",
            "fogis-save-cookies=fogis_session_tools.save_fogis_cookies:main",
            "fogis-check-status=fogis_session_tools.check_session_status:main",
        ],
    },
)
