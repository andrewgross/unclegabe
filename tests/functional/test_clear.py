# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch

from tests.helpers import get_cli, add_record


@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_clear_yes(user_input, output):
    """Clear should remove the queue when affirmed"""
    # When I have a queue with items
    cli = get_cli()
    add_record(cli, ("foo", 0))

    # And I confirm clearing a queue
    user_input.side_effect = ["Yes"]

    # Then I clear the queue
    cli.onecmd("clear")
    output.assert_called_once_with("Deleting queue test_shql")

    # And the queue has no items
    cli.onecmd("size")
    output.assert_called_with(0)


@patch('shql.shql.print_result')
@patch('shql.shql.get_input')
def test_clear_no(user_input, output):
    """Clear should not remove a queue when denied"""
    # When I have queue with items
    cli = get_cli()
    add_record(cli, ("foo", 0))

    # And I do not confirm clearing the queue
    user_input.side_effect = ["No"]

    # Then I do not clear the queue
    cli.onecmd("clear")
    output.assert_called_once_with("Aborting!")

    # And the queue has items
    cli.onecmd("size")
    output.assert_called_with(1)
