# -*- encoding: UTF-8 -*-
'''
Created on Mar 24, 2010

@author: maemo
'''

from zourite.core import plugin
import pickle
import logging
import gtk
import gtk.gdk
import datetime

import atom
import gdata.contacts
import gdata.contacts.service

from zourite.common import version


version.getInstance().submitRevision("$Revision: 105 $")

PLUGIN_NAME = "gmail"

class GmailPlugin(plugin.ZouritePlugin):
    '''
    The gmail plugin only provide contact on the address book of the gmail account.
    '''
    
    gmail_credential = None
   
    gd_client = None
    
    
    def _retrieve_gmail_credential(self):
        # essaye de charger l'acces token
        try:
            gmail_file = open(plugin.get_plugin_file_location(PLUGIN_NAME,'gmail_credential'),'rb');
            gmail_credential = pickle.load(gmail_file)
            gmail_file.close()
        except IOError:
            # pas d'acess token on en génère un autre
            raise plugin.ConfigurationRequiredExeption()            
    
        return gmail_credential;
    
    def _configure_gmail_account(self):
        '''
        launch the configuration wizard
        '''
        #TODO this is only a consol wizardn need to be more generic... 
        gc = GmailCredential()
        gc.email = raw_input("Please gmail account: ")
        gc.password = raw_input("Please gmail password: ")
        try:
            gmail_file = open(plugin.get_plugin_file_location(PLUGIN_NAME,'gmail_credential'),'wb');
            pickle.dump(gc,gmail_file)
            gmail_file.close()
        except IOError:
            logging.warning("the access token could not be saved")
        
        return gc
    
    #---------------------------------------------------------------------
    #
    # implementation de l'interface ZouritePlugin
    #
    #---------------------------------------------------------------------
        
    def get_plugin_id(self):
        return PLUGIN_NAME
    
    def configure(self):
        plugin.ensure_plugin_config_store_exist(PLUGIN_NAME)
        self.gmail_credential = self._configure_gmail_account()
      
    def getPluginLogoPixbuf(self):
        return gtk.gdk.pixbuf_new_from_file("gdata-contacts-icon.png")
    
    def run_plugin(self):
        self.gmail_credential = self._retrieve_gmail_credential()
        self.gd_client = gdata.contacts.service.ContactsService()
        self.gd_client.email = self.gmail_credential.email
        self.gd_client.password = self.gmail_credential.password
        self.gd_client.source = "bressure.net-zourite-1.0"
        self.gd_client.ProgrammaticLogin()

    def getMyConnections(self):
        allContacts = self.gd_client.GetContactsFeed().entry
        people = []       
        for entry in allContacts:
            p = ShortProfile(entry, self.gd_client.GetPhoto(entry))
            people.append(p)
        
        return people

    def getShortProfile(self, contactId):
        allContacts = self.gd_client.GetContactsFeed().entry
        selected = filter(lambda(x):x.id.text.rpartition("/")[2] == contactId, allContacts)        
        profile = ShortProfile(selected[0], self.gd_client.GetPhoto(selected[0]))
        return profile
   
    def getGdkPixbuf(self, shortProfile):
        return shortProfile.picture.getGdkPixbuf()
    
    def getGtkImage(self, shortProfile):
        '''
        return a gtk.Image for the profil
        '''
        
        return shortProfile.picture.getGtkImage() # return a pixbuf it's perhaps better

    def getNetworkUpdate(self):
       return []

    def getFullProfile(self, contactId):
       raise plugin.UnvailableException()

    def getMyStatus(self):
        return None
        
    def setMyStatus(self, status):
        pass





class GmailCredential():
    '''
    Simple objecy to store the gmail account credential
    '''
    email = ""
    password = ""

class Person(plugin.Person):
    
    def __init__(self, entry):
        plugin.Person.__init__(self)
        
        self.lastname= entry.title.text
               
        # TODO should choose the primary one
        organization = self._get_primary_organization(entry)
        if organization is not None :
            # Someyime the organization is an empty list
            if organization.org_title is not None:
                self.headline = organization.org_title.text
            if organization.org_name  is not None:
                self.headline = self.headline + " " + organization.org_name.text 
            
                                            
        self.networkId = PLUGIN_NAME
        self.id = entry.id.text.rpartition("/")[2]  # only the last part of this url will the id
        
    def _get_primary_organization(self, entry):
        '''
        Retrieve the primary organization or the first one 
        '''
        if isinstance(entry.organization,list):            
            if len(entry.organization) > 0:
                return entry.organization[0]
            else:
                return None
        elif isinstance(entry.organization, gdata.contacts.Organization):
            return entry.organization
        else:
            return None
    
        
class ShortProfile(Person, plugin.ShortProfile):
    
    def __init__(self, entry, hosted_image_binary):
        plugin.ShortProfile.__init__(self)
        Person.__init__(self, entry)
        
        if hosted_image_binary is None :
            self.picture = plugin.ImageProxyNone()
        else:
            filename = self.id
            file = plugin.get_plugin_file_location(PLUGIN_NAME, filename )
            image_file = open(file, 'wb')
            image_file.write(hosted_image_binary)
            image_file.close()
            self.picture = plugin.ImageProxyFile(PLUGIN_NAME, filename)

        # TODO should choose the work labeled one
        if len(entry.email) > 0 :
             self.email =  entry.email[0].address
        
        if len(entry.phone_number) > 0:
            self.phone = entry.phone_number[0].text
        
