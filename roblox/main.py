from urllib.request import urlopen, Request
from sys import version
import json
import ast
import urllib.parse as urlparse
from urllib.parse import urlencode

if version.startswith("3") is not True:
    raise ValueError("Please upgrade your python version. Current version is: {}".format(version))


user_api_version = "v1"
game_api_version = "v2"
group_api_version = "v2"

class Group:
    
    """
    A class to define a group WITHOUT a cookie/token aka (.ROBLOSECURITY)
    ---------
    Arguments
    groupID: The group id of a group.
    ---------
    Attributes
    ---------
    rawGroup: The request as a dict.
    hasVerifiedBadge: Returns if the group has a verified badge as a boolean.
    groupName: Returns the group's name.
    rawCreated: Returns the raw data from the request of the user's group created.
    UserDateCreated: Returns the date created of group.
    groupDescription: Returns the description of the group.
    """

    def __init__(self, groupID) -> None:

        try:
            int(groupID)
            self.userID = str(groupID)
        except ValueError:
            raise ValueError("Please have valid GroupID!")
        
        url = "https://groups.roblox.com/{}/groups".format(group_api_version)

        params = {'groupIds':'{}'.format(groupID)}

        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)

        url_parts[4] = urlencode(query)

        url = (urlparse.urlunparse(url_parts))
        httprequest = Request(url, headers={"Accept": "application/json"})

        with urlopen(httprequest) as response:
            if response.status != 200:
                raise ValueError("GroupId must be valid!")
            else:
                t = response.read().decode("utf-8")
                self.rawGroup = dict(json.loads(t))["data"]
        
        self.groupName = self.rawGroup[0]["name"]
        self.groupDescription = self.rawGroup[0]["description"]
        self.groupOwnerId = self.rawGroup[0]["owner"]["id"] if self.rawGroup[0]["owner"] != None else None
        self.groupDateCreated = self.rawGroup[0]["created"][:10]
        self.hasVerifiedBadge = bool(self.rawGroup[0]["hasVerifiedBadge"])
        self.rawCreated = self.rawGroup[0]["created"]
        self.GroupDateCreated = self.rawGroup["created"][:10]

class Player:

    """
    A class to define a user WITHOUT a cookie/token aka (.ROBLOSECURITY)
    ---------
    Arguments
    userID: The user id of a user.
    ---------
    Attributes
    ---------
    rawUser: The request as a dict.
    isBanned: Returns if the user is banned as a boolean.
    hasVerifiedBadge: Returns if the user has a verified badge as a boolean.
    UserName: Returns the user's username. Not to be confused with "DisplayName"
    DisplayName: Returns the user's display name.
    rawCreated: Returns the raw data from the request of the user's date created.
    UserDateCreated: Returns the date created of user.
    """
    def __init__(self, userID) -> None:

        try:
            int(userID)
            self.userID = str(userID)
        except ValueError:
            raise ValueError("Please have valid userID!")
           
        url = "https://users.roblox.com/{}/users/{}".format(user_api_version, userID)

        httprequest = Request(url, headers={"Accept": "application/json"})

        with urlopen(httprequest) as response:

            if response.status != 200:
                raise ValueError("UserId must be valid!")
            else:
                t = response.read().decode("utf-8")
                self.rawUser = dict(json.loads(t))
                
        self.userID = self.rawUser["id"]
        self.isBanned = True if self.rawUser["isBanned"] == "true" else False
        self.hasVerifiedBadge = True if self.rawUser["hasVerifiedBadge"] == "true" else False
        self.UserName = self.rawUser["name"]
        self.DisplayName = self.rawUser["displayName"]
        self.Description = self.rawUser["displayName"]
        self.rawUserCreated = self.rawUser["created"]
        self.UserDateCreated = self.rawUser["created"][:10]
