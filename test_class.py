from ConfluenceFiles.Confluence_api import Confluence
import config_file as config

args = {
    "space name" : "ipm",
    "space key" : "IPM",
    "title" : "Title 2",
    "description" : "this is the new page created by IPM",
    "query" : "intelligent"
}
c = Confluence(config.CONFLUENCE_BASE_URL, config.CONFLUENCE_ACCESS_TOKEN, config.CONFLUENCE_USER_EMAIL)
# c.getAllSpaces()
# c.createSpace(**args)
# c.getSpace(**args)
# c.updateSpaceDescription(**args)
# c.getSpaceContent(**args)
# c.createContent(**args)
# c.search(**args)