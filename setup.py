import setuptools

setuptools.setup(
    name='password-shack',
    version='1.0.0',
    author='Nithin P Manoj, Akshay K Biju, Gayathri Binoy',
    author_email='nithinp.manoj@gmail.com',
    description='Command line tool to create, store and retrieve passwords securely',
    url='https://github.com/nithinmanoj10/password-SHAck',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    zip_safe=False
)