"""TO-DO: Write a description of what this XBlock is."""

import pkg_resources
from django.utils.translation import ugettext_lazy as _

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
from xblockutils.resources import ResourceLoader
from xblockutils.settings import XBlockWithSettingsMixin
from xblockutils.studio_editable import StudioEditableXBlockMixin


LOADER = ResourceLoader(__name__)


@XBlock.wants("settings")
class ProgrammingConsoleXBlock(XBlock, XBlockWithSettingsMixin, StudioEditableXBlockMixin):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    display_name = String(
        display_name=_("Display Name"),
        scope=Scope.settings,
        default="Interactive Console",
    )

    hostname = String(
        display_name=_("Hostname"),
        scope=Scope.settings,
        default=None,
    )

    username = String(
        display_name=_("Username"),
        scope=Scope.settings,
        default=None,
    )

    password = String(
        display_name=_("Password"),
        scope=Scope.settings,
        default=None,
        help=_("Password must be encoded in base64"),
    )

    port = Integer(
        display_name=_("Port"),
        scope=Scope.settings,
        default=22,
    )

    editable_fields = (
        "display_name",
        "hostname",
        "username",
        "password",
        "port"
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the ProgrammingConsoleXBlock, shown to students
        when viewing courses.
        """
        in_studio_runtime = hasattr(
            self.xmodule_runtime, 'is_author_mode')  # pylint: disable=no-member

        if in_studio_runtime:
            return self.author_view(context)

        if not self.hostname or not self.username or not self.password or not self.port:
            frag = Fragment(u"The SSH client hasn't been set up. Go to the Studio component.")
            return frag

        context = {
            "hostname": self.hostname,
            "username": self.username,
            "password": self.password,
            "port": self.port,
        }

        frag = Fragment(
            LOADER.render_template(
                "static/html/programming_console.html", context
            )
        )
        frag.add_css(self.resource_string("static/css/programming_console.css"))
        frag.add_javascript(self.resource_string("static/js/src/programming_console.js"))
        frag.initialize_js('ProgrammingConsoleXBlock')
        return frag

    def author_view(self, context=None):
        """  Returns author view fragment on Studio """
        if not self.hostname or not self.username or not self.password or not self.port:
            frag = Fragment(u"The SSH client hasn't been set up. Go to the edit tab.")
            return frag


        frag = Fragment(u"All set up.")

        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
    @XBlock.json_handler
    def increment_count(self, data, suffix=''):
        """
        An example handler, which increments the data.
        """
        # Just to show data coming in...
        assert data['hello'] == 'world'

        self.count += 1
        return {"count": self.count}

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("ProgrammingConsoleXBlock",
             """<programming_console/>
             """),
            ("Multiple ProgrammingConsoleXBlock",
             """<vertical_demo>
                <programming_console/>
                <programming_console/>
                <programming_console/>
                </vertical_demo>
             """),
        ]
