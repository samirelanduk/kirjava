from setuptools import setup

setup(
 name="kirjava",
 version="0.1.2",
 description="A Python GraphQL client.",
 url="https://kirjava.samireland.com",
 author="Sam Ireland",
 author_email="mail@samireland.com",
 license="MIT",
 classifiers=[
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: MIT License",
  "Topic :: Internet",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.6",
  "Programming Language :: Python :: 3.7",
 ],
 keywords="GraphQL",
 py_modules=["kirjava"],
 install_requires=["requests"]
)
