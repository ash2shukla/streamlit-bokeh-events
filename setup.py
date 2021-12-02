import setuptools

setuptools.setup(
    name="streamlit-bokeh-events",
    version="0.1.3",
    author="Ashish Shukla",
    author_email="ash2shukla@gmail.com",
    description="A custom streamlit component to return js event values from bokeh plots to streamlit",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "bokeh>=2.4.1",
        "streamlit >= 0.63",
    ],
)
