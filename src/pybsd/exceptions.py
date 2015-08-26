# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import
import logging

__logger__ = logging.getLogger('pybsd')


class PyBSDError(Exception):
    """Base PyBSD Exception. It is only used to except any PyBSD error and never raised

    Attributes
    ----------
    msg : :py:class:`str`
        The template used to generate the exception message
    """
    msg = ''
    parameters = {}

    @property
    def message(self):
        """An alias of __str__, useful for tests"""
        return self.__str__()

    def __str__(self):
        # Returns the formatted msg as the string representation of the exception
        return self.msg.format(**self.parameters)


class MasterJailError(PyBSDError):
    """Base exception for errors involving a master and a jail. It is never raised

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : :py:class:`~pybsd.systems.jails.Jail`
        The jail
    """
    def __init__(self, master, jail):
        super(MasterJailError, self).__init__()
        self.parameters = {'master': master, 'jail': jail}


class AttachNonJailError(MasterJailError):
    """Error when a master tries to import a non-jail

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : `any`
        The object that was supposed to be attached
    """
    msg = u"Can't attach `{jail}` to `{master}`. `{jail}` is not a jail."


class JailAlreadyAttachedError(MasterJailError):
    """Error when a jail is already attached to another master

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : :py:class:`~pybsd.systems.jails.Jail`
        The jail
    """
    msg = u"Can't attach `{jail}` to `{master}`. `{jail}` is already attached to `{jail.master}`."


class DuplicateJailNameError(MasterJailError):
    """Error when another jail with the same name is already attached to a master

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : :py:class:`~pybsd.systems.jails.Jail`
        The jail
    """
    msg = u"Can't attach `{jail}` to `{master}`. A jail called `{jail.name}` is already attached to `{master}`."


class DuplicateJailHostnameError(MasterJailError):
    """Error when another jail with the same hostname is already attached to a master

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : :py:class:`~pybsd.systems.jails.Jail`
        The jail
    """
    msg = u"Can't attach `{jail}` to `{master}`. A jail with hostname `{jail.hostname}` is already attached to `{master}`."


class DuplicateJailUidError(MasterJailError):
    """Error when another jail with the same uid is already attached to a master

    Parameters
    ----------
    master : :py:class:`~pybsd.systems.masters.Master`
        The master
    jail : :py:class:`~pybsd.systems.jails.Jail`
        The jail
    """
    msg = u"Can't attach `{jail}` to `{master}`. A jail with uid `{jail.uid}` is already attached to `{master}`."


class CommandError(PyBSDError):
    """Base exception for errors involving a command. It is never raised

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.Command`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is deployed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    """
    def __init__(self, command, environment):
        super(CommandError, self).__init__()
        self.parameters = {'command': command, 'environment': environment}


class InvalidCommandNameError(CommandError):
    """Error when a command is missing a `name` attribute

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.Command`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is deployed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    """
    msg = "Can't initialize command: `{command.__class__.__module__}` is missing a `name` property."


class InvalidCommandExecutorError(CommandError):
    """Error when a command is missing a `name` attribute

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.Command`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is deployed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    """
    msg = "Can't initialize command: `{command}` must have a callable `Executor` method."


class CommandNotImplementedError(CommandError):
    """Error when a command is missing a `name` attribute

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.Command`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is deployed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    """
    msg = "Can't execute command: `{command}` is not implemented on `{environment}`."


class CommandConnectionError(CommandError):
    """Error when a command is missing a `name` attribute

    Parameters
    ----------
    command : :py:class:`~pybsd.commands.Command`
        The command
    environment : :py:class:`~pybsd.systems.base.BaseSystem`
        The environment on which the command is deployed. Any subclass of :py:class:`~pybsd.systems.base.BaseSystem`
    """
    msg = "Can't execute command: `{command}`- can't connect to `{environment}`."
