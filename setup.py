from setuptools import setup, find_packages

setup(
    name='wagtail_site',
    version='0.4.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=4.2',
        'django-widget-tweaks>=1.5.0',
        'django-modelcluster>=6.4',
        'django-taggit>=6.1.0',
        'wagtail>=6.4.1',
        'wagtail-localize>=1.12.1',
    ],
    author='Antwi Kwarteng',
    description='A reusable Django app for creating wagtail websites.',
)
