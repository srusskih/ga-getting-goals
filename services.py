import atom
import gdata
import gdata.analytics.client


class ManagementService(gdata.service.GDataService):
    def __init__(self, email="", password=None, source=None,
               server='www.google.com/analytics', additional_headers=None,
               **kwargs):
        """Creates a client for the Google Analytics service.

        Args:
          email: string (optional) The user's email address, used for
              authentication.
          password: string (optional) The user's password.
          source: string (optional) The name of the user's application.
          server: string (optional) The name of the server to which a connection
              will be opened.
          **kwargs: The other parameters to pass to gdata.service.GDataService
              constructor.
        """

        gdata.service.GDataService.__init__(
            self, email=email, password=password, service='analytics',
            source=source, server=server, additional_headers=additional_headers,
            **kwargs)

    def GetGoalsList(self, *args, **kwrags):
        resonse = self.Get(self.GoalsUri(*args, **kwrags))
        return atom.core.parse(resonse.ToString(), gdata.analytics.data.ManagementFeed)

    def GoalsUri(self, *args, **kwrags):
        return str(gdata.analytics.client.GoalQuery(*args, **kwrags))

