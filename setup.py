import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="telegram",
    version="0.0.1",
    author="Maximilian Clemens",
    description="Simple Telegram Bot Library",
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires='>=3.10',
    url='https://github.com/MaximilianClemens/pytelegram',
    license='MIT',
    keywords=['telegram', 'chatbot']
)
