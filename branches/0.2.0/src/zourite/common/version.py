# -*- encoding: UTF-8 -*-
'''
Created on 28 mars 2010

@author: thierry
'''



CURRENT_VERSION = "0.2.0-3"  # this must be modified before any release

def getInstance():
    return SINGLETON

class Version(object):
    '''
    Hold the revision of the application.
    '''        

    def __init__(self):
        '''
        Constructor
        '''
        self.revision = ""
        
    def submitRevision(self, rev):
        '''
        submit a new revision. If the revision is upper than
        the current revision, it become the new current revision
        '''
        
        if self.revision < rev:
            self.revision = rev
            
    def getRevision(self):
        '''
        Return the scm revision for this application
        '''
        return self.revision
    
    def getVersion(self):
        '''
        Return the marketing version for this application.
        '''
        return CURRENT_VERSION
    
SINGLETON = Version()  # object that track the revision of current applcation for issue tracking purpose

getInstance().submitRevision("$Revision: 174 $")
