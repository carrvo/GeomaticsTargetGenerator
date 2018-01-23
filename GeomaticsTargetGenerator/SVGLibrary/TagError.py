"""
"""

class TagError(NameError):
    """
    """

    def __init__(self, tag, proper_name):
        """
        Initializes.
        """
        self.tag = tag
        self.args = (proper_name,)

    def __str__(self):
        return 'Tag is not a "{}" it is a "{}"'.format(self.args[0], self.tag.name)
    __str__.__doc__ = object.__str__.__doc__
