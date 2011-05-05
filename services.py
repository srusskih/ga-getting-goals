import atom
import gdata
import gdata.analytics.client

GAN_NAMESPACE = gdata.analytics.GAN_NAMESPACE
GA_NAMESPACE = 'http://schemas.google.com/ga/2009'


class Engagement(gdata.GDataEntry):
    """
        ``comparison`` - The comparison: > or < or =
        ``thresholdValue`` - The value that triggers the goal
        ``type`` - The type of engagement for the goal: timeOnSite or pagesVisited
    """
    _tag = 'engagement'
    _namespace = GA_NAMESPACE
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()

    _attributes['comparison'] = 'comparison'
    _attributes['thresholdValue'] = 'thresholdValue'
    _attributes['type'] = 'type'

    def __init__(self, comparison=None, thresholdValue=0,
            type=None, *args, **kwargs):
        self.comparison = comparison
        self.thresholdValue = thresholdValue
        self.type = type
        super(Engagement, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.type


class Step(gdata.GDataEntry):
    """
        ``name`` - The step name
        ``number`` - The step number
        ``path`` - The step path
    """
    _tag = 'step'
    _namespace = GA_NAMESPACE
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()

    _attributes['name'] = 'name'
    _attributes['number'] ='number'
    _attributes['path'] ='path'

    def __init__(self, name=None, number=0, path=None, *args, **kwargs):
        self.name = name
        self.number = number
        self.path = path
        super(Step, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.name


class Destination(gdata.GDataEntry):
    """
        ``caseSensitive`` - Whether path URL matching is case sensitive
        ``expression`` - The goal path to match 
        ``matchType`` - The match type for the path expression, either head, regex, or exact
        ``step1Required`` - Whether Step 1 is required
    """
    _tag = 'destination'
    _namespace = GA_NAMESPACE
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()

    _attributes['caseSensitive'] = 'caseSensitive'
    _attributes['expression'] = 'expression'
    _attributes['matchType'] = 'matchType'
    _attributes['step1Required'] = 'step1Required'
    _attributes['{%s}step' % GA_NAMESPACE] = ('step', [Step])

    def __init__(self, caseSensitive=False, expression=None,
            matchType=None, step1Required=False, step=None, *args, **kwargs):
        self.caseSensitive = caseSensitive
        self.expression = expression
        self.matchType = matchType
        self.step1Required = step1Required
        self.step = step
        super(Destination, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.expression


class Goal(gdata.GDataEntry):
    """
        ``active`` - Indicates whether the goal is active or not
        ``name`` - The goal name
        ``number`` - The goal number
        ``value`` - The goal value

        Note: Current goal fields will have either ``destination`` or ``engagement`` as children, but not both.
        Since API exposure of future Analytics goals is not immediate, your code should
        explicitly check if the goal has a ``destination`` or ``engagement`` child elements before trying to access it.
    """
    _tag = 'goal'
    _namespace = GA_NAMESPACE
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()

    _attributes['name'] = 'name'
    _attributes['value'] = 'value'
    _attributes['number'] = 'number'
    _attributes['active'] = 'active'
    _children['{%s}destination' % GA_NAMESPACE] = ('destination', Destination)
    _children['{%s}engagement' % GA_NAMESPACE] = ('engagement', Engagement)

    def __init__(self, name=None, active=False, number=0, value=0.0,
            destination=None, engagement=None, *args, **kwargs):
        self.name = name
        self.active = active
        self.number = number
        self.value= value
        self.destination = destination
        self.engagement = engagement
        super(Goal, self).__init__(*args, **kwargs)

    def __str__(self):
        return self.value

    def __repr__(self):
        return '<Goal: %s %s>' % (self.name, self.value)


class GoalFeedListEntry(gdata.GDataEntry):
    _tag = 'entry'
    _namespace = atom.ATOM_NAMESPACE
    _children = gdata.GDataEntry._children.copy()
    _attributes = gdata.GDataEntry._attributes.copy()
    _children['{%s}goal' % GA_NAMESPACE] = ('goal', Goal)
    _children['{%s}property' % GAN_NAMESPACE] = ('property', gdata.analytics.Property)

    def __init__(self, goal=None, property=None, *args, **kwargs):
        self.goal = goal
        self.property = property
        super(GoalFeedListEntry, self).__init__(*args, **kwargs)


class GoalFeedList(gdata.GDataFeed):
    _tag = 'feed'
    _namespace = atom.ATOM_NAMESPACE
    _children = gdata.GDataFeed._children.copy()
    _attributes = gdata.GDataFeed._attributes.copy()
    _children['{%s}entry' % atom.ATOM_NAMESPACE] = ('entry', [GoalFeedListEntry])


def GoaltFeedListFromString(xml_string):
    """Converts an XML string into an ManagementEntry object.

    Args:
    xml_string: string The XML describing a Document List feed entry.

    Returns:
      A ManagementEntry object corresponding to the given XML.
    """
    return atom.CreateClassFromXMLString(GoalFeedList, xml_string)


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
        uri = self.GoalsUri(*args, **kwrags)
        return self.Get(uri, converter=GoaltFeedListFromString)

    def GoalsUri(self, *args, **kwrags):
        return str(gdata.analytics.client.GoalQuery(*args, **kwrags))

