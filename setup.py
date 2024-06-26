from setuptools import setup, find_packages

setup(
    name="network_com",
    version="1.2.3b1",
    packages=find_packages(),
    install_requires=[
        "inputimeout"
    ],
    entry_points={
        'console_scripts': [
            'run-client=network_com.client:udp_listener',
            'run-server=network_com.server:send_ip'
        ]
    },
    author="Karam Belmoujoud",
    author_email="karam.bd.kb@gmail.com",
    description="A package for client-server communication over TCP and UDP",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KaramBelmoujoud/Multi-Client-TCP-UDP-Communication-Server-in-Python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
