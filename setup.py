from setuptools import setup

setup(name='EditorConfigGitPreserveHistory',
      version='0.1',
      description='Commit changes from editorconfig and preserve authorship',
      long_description=open('README.rst').read(),
      url='http://github.com/dmeybohm/editorconfig-git-preserve-history',
      author='David Meybohm',
      author_email='dmeybohm@gmail.com',
      license='MIT',
      packages=['editorconfig_git_preserve_history'],
      install_requires=[
          'EditorConfig>=0.12.1',
      ],
      scripts=['bin/editorconfig-git-preserve-history'],
      test_suite='nose.collector',
      tests_require=['nose'])
