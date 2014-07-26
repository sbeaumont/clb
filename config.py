import sys
import os

def appendPath(relativePath):
    """Add library directory to search path relative to this file.
    Don't pass in a string with separators e.g. 'lib/requests'.
    Pass in a list of path parts to ensure correct OS separator, e.g. ('lib', 'requests').
    You may pass in a simple string for one path part, e.g. 'lib'.
 """
    realPath = os.path.realpath(__file__)
    dirName = os.path.dirname(realPath)
    
    if isinstance(relativePath, basestring):
        joinedPath = os.path.join(dirName, relativePath)
    else:
        joinedPath = os.path.join(dirName, *relativePath)
        
    sys.path.append(joinedPath)

    return joinedPath    

# Add the libraries to the search path as a tuple of path parts.

# Requests library: http://docs.python-requests.org/en/latest/
appendPath( ("lib", "requests") )


if __name__ == "__main__":
    # Simple unit tests
    assert os.path.isdir(appendPath("lib"))
    assert os.path.isdir(appendPath("lib/requests"))
    assert os.path.isdir(appendPath( ("lib", "requests") ))
