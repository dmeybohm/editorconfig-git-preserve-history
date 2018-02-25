from setuptools import setup

setup(name='EditorConfigGitPreserveHistory',
      version='0.1',
      description='Commit changes to editorconfig and preserve authorship',
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
