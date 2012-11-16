from fabric.api import local
from fabric.operations import prompt


def package():
    '''
    Pacakge htseq-count for upload to toolshed
    '''
    version = prompt("Enter version number for package [test]:")
    revision = ''
    if version != '':
        revision = '-r "%s"' % version
    else:
        version = 'test'
    local('mkdir -p package')
    local('rm -f package/ea-utils_%s.tar.gz' % version)
    if version == 'test':
        local('tar czvf package/ea-utils_%s.tar.gz --exclude "fabfile.*" --exclude "package" --exclude ".hg" *' % version)
    else:
        local('hg archive -t tgz %s -X "fabfile.*" -X "package" -p . "package/ea-utils_%s.tar.gz"' % (revision, version))
