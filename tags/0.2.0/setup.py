# -*- encoding: UTF-8 -*-
'''
Created on 30 mars 2010

@author: thierry
'''
from distutils.core import setup
setup(name='zourite',
      version='0.2.0',
      package_dir = {'': 'src'},
      packages=['zourite',
                'zourite.common',
                'zourite.core',
                'zourite.gui',
                'zourite.plugin',
                'zourite.plugin.gmail',
                'zourite.plugin.linkedin'],
      scripts=['scripts/zourite','scripts/zourite-setup','scripts/zourite-setup-force'],
      package_data={'zourite': ['*.png']},      
      author='Thierry Bressure',
      author_email='thierry@bressure.net',
      maintainer='Thierry Bressure',
      maintainer_email='zourite@bressure.net',
      url='http://blog.zourite.bressure.net',
      download_url='http://zourite.bressure.net',
      description='Zourite Professional Networking Application for N900',
      long_description='Zourite is a client for professional Network like LinkedIn. You can stay connected to your contacts and manage you network.',
      classifiers=[
          'Development Status :: 1',
          'Environment :: Hildon',
          'Environment :: Maemo',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',          
          'License :: OSI Approved :: LGPL',
          'Operating System :: Maemo :: Maemo 5',
          'Programming Language :: Python',
          'Topic :: Communications :: Email',
          'Topic :: Office/Business',          
          ],

      )


