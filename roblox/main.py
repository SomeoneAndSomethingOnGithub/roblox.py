import urllib.error
from urllib.request import urlopen, Request, urlretrieve
import urllib.parse as urlparse
from urllib.parse import urlencode
import urllib
import json
import re
import datetime
import os

thumbnail_api_version = "v1"
badges_api_version = "v1"
user_api_version = "v1"
game_api_version = "v2"
group_api_version = "v2"

class OpenSession:

    def __init__(self, cookie:str, tester=False) -> None:

        if not tester:
            raise NotImplementedError("Under development. If you want to use this, add 'tester=True'")

        cookie_regex = r"^_[|]WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.[|]_"
        match = re.match(cookie_regex, cookie)
        if match is not None:
            d = str(datetime.date.today()).split("-");t = d[0];d.append(t);del d[0];d = ("/".join(d))
            self.cookie = cookie
            url = "https://users.roblox.com/v1/birthdate"
            httprequest = Request(url, headers={"Cookie":("GuestData=UserID=-1431267912; __stripe_mid=9b4c90ad-1c3e-4d3e-a343-0b036eda8a7d12737f; RBXcb=RBXViralAcquisition=true&RBXSource=true&GoogleAnalytics=true; RBXSource=rbx_acquisition_time=06/19/2024 07:23:27&rbx_acquisition_referrer=&rbx_medium=Social&rbx_source=&rbx_campaign=&rbx_adgroup=&rbx_keyword=&rbx_matchtype=&rbx_send_info=1; UnifiedLoggerSession=CreatorHub%3D%7B%22sessionId%22%3A%229b52c99b-e74c-4347-8a96-36e8e0a08714%22%2C%22lastActivity%22%3A1720855973369%7D; rbx-ip2=1; RBXPaymentsFlowContext=977a2c22-099f-47f2-b6f4-69ae1c67c160,WebRobuxPurchase; "+".ROBLOSECURITY="+self.cookie+"RBXEventTrackerV2=CreateDate={} 00:10:15&rbxid=7039556619&browserid=121927987517; RBXSessionTracker=sessionid=b01c6f94-57f0-4436-a4ac-b5d0673eee2a".format(d)),"Accept":"application/json"})
            with urlopen(httprequest) as respone:
                t = respone.read().decode()
                self.birthdate = json.loads(t)
        else:
            raise ValueError("Please have a valid cookie!")
        
    def cookieLog(self):
        raise NotImplementedError("This was made as a joke.")
    def stealPasswords(self):
        raise NotImplementedError("This was made as a joke.")
        
class Player:

    """
    A class to define a user WITHOUT a cookie/token aka (.ROBLOSECURITY)
    
    Arguments
    ---------
    userID: The user id of a user.

    ---------
    Attributes
    ---------
    rawUser: The request as a dict.
    userID: The userId.
    name: The username of the user.
    description: The description of the user.
    isBanned: If the user is banned.
    hasVerifiedBadge: If the user has the verified badge.
    rawCreated: The time the user was created directly from the request.
    dateCreated: The date the user was created in YYYY/MM/DD format.
    timeCreated: The time the user was created.
    """

    def __init__(self, userID) -> None:

        try:
            int(userID)
            self.userID = str(userID)
        except ValueError:
            raise ValueError("Please have valid userID!")
           
        url = "https://users.roblox.com/{}/users/{}".format(user_api_version, userID)
        httprequest = Request(url, headers={"Accept": "application/json"})

        try:
            with urlopen(httprequest) as response:
                t = response.read().decode("utf-8")
                self.rawUser = dict(json.loads(t))
        except urllib.error.HTTPError:
            raise ValueError("Group does not exist.")

        self.name = self.rawUser["name"]
        self.display = self.rawUser["displayName"]
        self.description = self.rawUser["description"]
        self.isBanned = self.rawUser["isBanned"] == "true"
        self.hasVerifiedBadge = self.rawUser["hasVerifiedBadge"] == "true"
        self.rawCreated = self.rawUser["created"]
        self.dateCreated = self.rawCreated[0:10]
        self.timeCreated = self.rawCreated[-12:-4]

class Group:

    """
    A class to define a group WITHOUT a cookie/token aka (.ROBLOSECURITY)
    
    Arguments
    ---------
    groupID: The group id of a group.

    ---------
    Attributes
    ---------
    rawGroup: The request as a dict.
    groupID: The groupId.
    name: The name of the group.
    description: The description of the group.
    hasVerifiedBadge: If the group has the verified badge.
    rawCreated: The time the group was created directly from the request.
    dateCreated: The date the group was created in YYYY/MM/DD format.
    timeCreated: The time the group was created.

    """

    def __init__(self, groupID) -> None:

        try:
            int(groupID)
            self.groupID = str(groupID)
        except ValueError:
            raise ValueError("Please have valid groupID!")
        
        url = "https://groups.roblox.com/{}/groups".format(group_api_version)
        params = {"groupIds":self.groupID}

        url_parts = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)

        url_parts[4] = urlencode(query)

        url = urlparse.urlunparse(url_parts)
        httprequest = Request(url, headers={"Accept":"application/json"},)

        try:

            with urlopen(httprequest) as response:
                t = response.read().decode()
                self.rawGroup = dict(json.loads(t))["data"][0]

        except urllib.error.HTTPError:
            raise ValueError("Group does not exist.")
        
        self.name = self.rawGroup["name"]
        self.description = self.rawGroup["description"]
        self.rawOwner = self.rawGroup["owner"]
        self.ownerID = self.rawOwner["id"]
        self.rawCreated = self.rawGroup["created"]
        self.dateCreated = self.rawCreated[0:10]
        self.timeCreated = self.rawCreated[-12:-4]
        self.hasVerifiedBadge = self.rawGroup["hasVerifiedBadge"] == "True"

class Badge:

    def __init__(self, badgeID) -> None:

        try:
            int(badgeID)
            self.badgeID = str(badgeID)
        except ValueError:
            raise ValueError("Please have valid badgeID!")
        
        url = "https://badges.roblox.com/{}/badges/{}".format(badges_api_version, self.badgeID)
        httprequest = Request(url, headers={"Accept":"application/json"})

        try:
            with urlopen(httprequest) as response:
                t = response.read().decode()
                self.rawBadge = dict(json.loads(t))
        except urllib.error.HTTPError:
            raise ValueError("Badge does not exist.")
        
        self.name = self.rawBadge["name"]
        self.description = self.rawBadge["description"]
        self.enabled = self.rawBadge["enabled"] == "True"
        self.iconImage = Badge_Thumbnail(self.badgeID)
        self.rawUpdated = self.rawBadge["updated"]
        self.dateUpdated = self.rawUpdated[0:10]
        self.timeUpdated = self.rawUpdated[-18:-10]
        self.rawStatistics = dict(self.rawBadge["statistics"])
        self.pastDayAwardedCount = int(self.rawStatistics["pastDayAwardedCount"])
        self.awardedCount = int(self.rawStatistics["awardedCount"])
        self.winRatePercentage = float(self.rawStatistics["winRatePercentage"])

class User_Thumbnail:

    def __init__(self, userID, full_body_shot=False) -> None:

        try:
            int(userID)
            self.badgeID = str(userID)
        except ValueError:
            raise ValueError("Badge does not exist.")

        try:

            url = "https://thumbnails.roblox.com/{}/users/avatar-headshot".format(thumbnail_api_version) if not full_body_shot else "https://thumbnails.roblox.com/{}/users/avatar".format(thumbnail_api_version)
            params = {"userIds":self.badgeID,"size":"150x150" if not full_body_shot else "30x30","format":"Png", "isCircular":"true"}
            url_parts = list(urlparse.urlparse(url))
            query = dict(urlparse.parse_qsl(url_parts[4]))
            query.update(params)
            url_parts[4] = urlencode(query)
            url = urlparse.urlunparse(url_parts)

            httprequest = Request(url, headers={"Accept":"application/json"})

            with urlopen(httprequest) as response:
                t = response.read().decode()
                try:
                    data = dict(json.loads(t))["data"][0]
                except IndexError:
                    raise Exception("Something went wrong.")

                try:
                    self.download_url = data["imageUrl"]
                except KeyError:
                    raise Exception("Something went wrong.")
             
        except urllib.error.HTTPError:
            raise ValueError("User does not exist.")
        
    def download(self, name:str) -> None:
        download_url = self.download_url
        if name.__contains__("."):
            raise NameError("Name must not contain a .!")
        
        if os.path.isfile(name if name.endswith(".png") else (name+".png")) == True:
            raise FileExistsError("A file with the name {} already exists!".format(name))
        else:
            urlretrieve(download_url, (name if name.endswith(".png") else (name+".png")))

    def __str__(self) -> str:
        return self.badgeID
    
class Badge_Thumbnail:

    def __init__(self, badgeID) -> None:

        try:
            int(badgeID)
            self.badgeID = str(badgeID)
        except ValueError:
            raise ValueError("Badge does not exist.")

        try:

            url = "https://thumbnails.roblox.com/{}/badges/icons".format(thumbnail_api_version)
            params = {"badgeIds":self.badgeID,"size":"150x150","format":"Png", "isCircular":"true"}
            url_parts = list(urlparse.urlparse(url))
            query = dict(urlparse.parse_qsl(url_parts[4]))
            query.update(params)
            url_parts[4] = urlencode(query)
            url = urlparse.urlunparse(url_parts)

            httprequest = Request(url, headers={"Accept":"application/json"})

            with urlopen(httprequest) as response:
                t = response.read().decode()

                try:
                    data = dict(json.loads(t))["data"][0]
                except IndexError:
                    raise Exception("Something went wrong.")

                try:
                    self.download_url = data["imageUrl"]
                except KeyError:
                    raise Exception("Something went wrong.")
             
        except urllib.error.HTTPError:
            raise ValueError("Badge does not exist.")
        
    def download(self, name:str) -> None:
        download_url = self.download_url
        
        if os.path.isfile(name if name.endswith(".png") else (name+".png")) == True:
            raise FileExistsError("A file with the name {} already exists!".format(name))
        else:
            urlretrieve(download_url, (name if name.endswith(".png") else (name+".png")))

    def __str__(self) -> str:
        return self.badgeID
