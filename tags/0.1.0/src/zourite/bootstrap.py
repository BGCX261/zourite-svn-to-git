# -*- encoding: UTF-8 -*-

'''
Created on 9 mars 2010

@author: thierry
'''

import sys

from zourite.core import zourite,plugin
from zourite.plugin.linkedin import linkedinplugin
from zourite.plugin.gmail import gmailplugin


from zourite.common import version


version.getInstance().submitRevision("$Revision: 112 $")


class AllPluginBootstrap():
    PLUGIN_LIST = [linkedinplugin.LinkedInPlugin(), gmailplugin.GmailPlugin()]
    
    def boot(self):
        zourite.ZOURITE_AVAILABLE_PLUGIN = self.PLUGIN_LIST



def runGui(argline=[]):
    
    from zourite.gui.zouriteGui import ZouriteGui 
    
    app = None
    if len(argline) > 1:
        if argline[1] == "mock":
            app = ZouriteGui(True)
        else:
            logging.warning("unknown argument " + argline[1] + ", ignored")
            bootstrap.AllPluginBootstrap().boot()
            app = ZouriteGui(False)
    else:   
        AllPluginBootstrap().boot()             
        app = ZouriteGui()
    # the hui is up and visible, so let's play
    app.run()
    
def runSetup():
    '''
    This method should be run only if no plugin have been registered yet.
    This method try to load each plugin and mark them as registered e.g.
    to be load when zourite is instanciated.
    '''
    AllPluginBootstrap().boot() # inject all available plugin
    zcore = zourite.Zourite(auto_load=False) # create an instance of the core
    zcore.applyDefaultSettings()    
    for aPlugin in zourite.ZOURITE_AVAILABLE_PLUGIN: # for each available plugin
        try:
            zcore.register_plugin(aPlugin) # register the plugin
        except plugin.ConfigurationRequiredExeption:
            aPlugin.configure()
            zcore.register_plugin(aPlugin)

    zcore.save_registered_plugin() # save the current configuration of registered plugins
                
        
if __name__ == "__main__":
        
    
    
    # check arg line if mock mode is required    
    argline = sys.argv
    if len(argline) > 1 and argline[1] == "setup":
        runSetup()
    else:
        runGui(argline)
    
    