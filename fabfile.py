from fabric.api import local
from fabric.operations import prompt


def package():
    '''
    Pacakge htseq-count for upload to toolshed
    '''
    version = prompt("Enter version number for package:")
    local('mkdir -p package')
    local('rm -f package/ea-utils_%s.tar.gz' % version)
    #local('tar czvf package/ea-utils_%s.tar.gz --exclude "fabfile.*" --exclude "package" --exclude ".hg" *' % version)
    local('hg archive -t tgz -r "%s" -X "fabfile.*" -X "package" -p . "package/ea-utils_%s.tar.gz"' % (version, version))
