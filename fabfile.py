from fabric.api import local

def package():
    '''
    Pacakge htseq-count for upload to toolshed
    '''
    local('rm package/htseq-count.tar.gz')
    local('tar czvf package/htseq-count.tar.gz --exclude "fabfile.*" --exclude "package" --exclude ".hg" *')
