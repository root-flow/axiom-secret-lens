from setuptools import setup, find_packages

setup(
    name="axiom-secret-lens",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[], # Şu an dış kütüphane kullanmadık, tertemiz.
    entry_points={
        'console_scripts': [
            'asl=asl:main', # Terminale sadece 'asl' yazınca çalışmasını sağlar
        ],
    },
    author="root-flow",
    description="A post-exploitation memory scanner for secrets",
    url="https://github.com/root-flow/axiom-secret-lens",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
