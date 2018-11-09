from setuptools import setup, find_packages

version = "2.0.2"

setup(name='geobuf',
      version=version,
      description=(
          u"Geobuf is a compact binary geospatial format for lossless "
          u"compression of GeoJSON and TopoJSON data."),
      classifiers=[],
      keywords='data gis geojson topojson protobuf',
      author=u"Vladimir Agafonkin",
      author_email='vladimir@mapbox.com',
      url='https://github.com/mapbox/pygeobuf',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['click', 'protobuf', 'six'],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      geobuf=geobuf.scripts.cli:cli
      """)
