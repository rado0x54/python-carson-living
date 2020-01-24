"""Module containing all devices that are exposed via Carson Living"""

import logging
from abc import ABCMeta, abstractmethod

from carson_living.error import CarsonError

_LOGGER = logging.getLogger(__name__)


class _AbstractEntity(object):
    # pylint: disable=useless-object-inheritance
    """Updateable Base Entity

    Attributes:
        _update_callback:
            The callback that can be used to update the
            entity_payload:
        _entity_payload:
            The payload the the entity draws its internal
            state from.

    """
    __metaclass__ = ABCMeta

    def __init__(self, update_callback=None, entity_payload=None):
        self._update_callback = update_callback
        # Note, entity_payload is written in self.update()
        self._entity_payload = None

        # update internal representation
        self.update(entity_payload)

    def __repr__(self):
        return '{} with unique_entity_id {}'.format(
            self.__class__.__name__, self.unique_entity_id)

    @property
    @abstractmethod
    def entity_id(self):
        """Entity ID

        Returns:
            Domain-specific entity id.

        """
        raise NotImplementedError(
            'Derived Entity does not implement entity_id!')

    @property
    @abstractmethod
    def unique_entity_id(self):
        """Unqiue Entity ID

        Returns:
            Unique entity id across entire library.
        """
        raise NotImplementedError(
            'Derived Entity does not implement unique_entity_id!')

    @abstractmethod
    def _internal_update(self):
        """Update internal state

        Allows the entity to update internal state
        after _entity_payload changes
        """
        raise NotImplementedError(
            'Derived Entity does not implement _internal_update!')

    @property
    def entity_payload(self):
        """Entity Payload

        Returns: the raw entity_payload

        """
        return self._entity_payload

    def update(self, entity_payload=None):
        """Update the entity

        Updates the entity with a given entity_payload. This payload
        can be passed directly the update function OR if left empty,
        the entity updates via tha given update_callback

        Args:
            entity_payload: optional payload to setup the entity

        Raises:
            CarsonError:
                If neither a entity_payload or a update_callback
                was passes during initialization.

        """
        # If there is a entity_payload, use it over the callback.
        if entity_payload:
            self._entity_payload = entity_payload
            # Allow child class to perform internal updates
            self._internal_update()
            return

        if not self._update_callback:
            raise CarsonError(
                'Trying to update entity {} without external payload '
                'or a callback function'
                .format(self.unique_entity_id))

        _LOGGER.info(
            'Trying to updated entity %s from update callback',
            self.unique_entity_id)
        self._entity_payload = self._update_callback()

        # Allow child class to perform internal updates
        self._internal_update()


class _AbstractAPIEntity(_AbstractEntity):
    # pylint: disable=abstract-method
    __metaclass__ = ABCMeta

    def __init__(self, api, update_callback=None, entity_payload=None):
        self._api = api
        super(_AbstractAPIEntity, self).__init__(
            update_callback=update_callback,
            entity_payload=entity_payload)
