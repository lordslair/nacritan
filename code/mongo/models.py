# -*- coding: utf8 -*-

import datetime
import uuid

from mongoengine import (
    Document,
    # EmbeddedDocument,
    )
from mongoengine.fields import (
    # BooleanField,
    DateTimeField,
    # EmbeddedDocumentField,
    IntField,
    # DictField,
    # ListField,
    # ReferenceField,
    StringField,
    UUIDField,
)


class TileDocument(Document):
    """
    Define the document for: Tile

    Fields:
    - _id       (UUIDField)
    - created   (DateTimeField)
    - type      (StringField)
    - updated   (DateTimeField)
    - user      (StringField)
    - x         (IntField)
    - y         (IntField)
    """
    _id = UUIDField(binary=False, primary_key=True, default=uuid.uuid4())
    created = DateTimeField(default=datetime.datetime.utcnow)
    type = StringField(required=True)
    updated = DateTimeField(default=datetime.datetime.utcnow)
    user = StringField(required=True)
    x = IntField(required=True)
    y = IntField(required=True)

    meta = {
        'collection': 'tiles',
        'indexes': [],
    }


class ResourceDocument(Document):
    """
    Define the document for: Resource

    Fields:
    - _id       (UUIDField)
    - created   (DateTimeField)
    - level     (IntField)
    - name      (StringField)
    - type      (StringField)
    - updated   (DateTimeField)
    - user      (StringField)
    - x         (IntField)
    - y         (IntField)
    """
    _id = UUIDField(binary=False, primary_key=True, default=uuid.uuid4())
    created = DateTimeField(default=datetime.datetime.utcnow)
    level = IntField(required=True)
    name = StringField(required=True)
    updated = DateTimeField(default=datetime.datetime.utcnow)
    user = StringField(required=True)
    x = IntField(required=True)
    y = IntField(required=True)

    meta = {
        'collection': 'resources',
        'indexes': [],
    }


class ObjectDocument(Document):
    """
    Define the document for: Object

    Fields:
    - _id       (IntField)
    - created   (DateTimeField)
    - name      (StringField)
    - updated   (DateTimeField)
    - type      (StringField)
    - user      (StringField)
    - x         (IntField)
    - y         (IntField)
    """
    _id = IntField(primary_key=True, required=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    name = StringField(required=True)
    updated = DateTimeField(default=datetime.datetime.utcnow)
    user = StringField(required=True)
    x = IntField(required=True)
    y = IntField(required=True)

    meta = {
        'collection': 'objects',
        'indexes': [],
    }


class MonsterDocument(Document):
    """
    Define the document for: Monster

    Fields:
    - _id       (IntField)
    - created   (DateTimeField)
    - level     (IntField)
    - name      (StringField)
    - updated   (DateTimeField)
    - user      (StringField)
    - wounds    (StringField)
    - x         (IntField)
    - y         (IntField)
    """
    _id = IntField(primary_key=True, required=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    level = IntField(required=True)
    name = StringField(required=True)
    updated = DateTimeField(default=datetime.datetime.utcnow)
    user = StringField(required=True)
    wounds = StringField(required=True)
    x = IntField(required=True)
    y = IntField(required=True)

    meta = {
        'collection': 'monsters',
        'indexes': [],
    }


class PlaceDocument(Document):
    """
    Define the document for: Place

    Fields:
    - _id       (IntField)
    - created   (DateTimeField)
    - level     (IntField)
    - name      (StringField)
    - townId    (IntField)
    - townName  (StringField)
    - updated   (DateTimeField)
    - user      (StringField)
    - x         (IntField)
    - y         (IntField)
    """
    _id = IntField(primary_key=True, required=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    level = IntField(required=True)
    name = StringField(required=True)
    townId = IntField()
    townName = StringField()
    updated = DateTimeField(default=datetime.datetime.utcnow)
    user = StringField(required=True)
    x = IntField(required=True)
    y = IntField(required=True)

    meta = {
        'collection': 'places',
        'indexes': [],
    }


class PlayerDocument(Document):
    """
    Define the document for: Player

    Fields:
    - _id       (IntField)
    - created   (DateTimeField)
    - guildId   (IntField)
    - guildName (StringField)
    - level     (IntField)
    - name      (StringField)
    - updated   (DateTimeField)
    - user      (StringField)
    - wounds    (StringField)
    - x         (IntField)
    - y         (IntField)
    - race      (StringField)
    - img       (StringField)
    - dla       (StringField)
    - pas       (StringField)
    - pos       (StringField)
    - xp        (StringField)
    - xpMax     (StringField)
    - pv        (IntField)
    - pvMax     (IntField)
    - attM      (IntField)
    - defM      (IntField)
    - degM      (IntField)
    - arm       (IntField)
    - mmM       (IntField)
    - pc        (IntField)
    """
    _id = IntField(primary_key=True, required=True)
    created = DateTimeField(default=datetime.datetime.utcnow)
    guildId = IntField(required=False, default=None)
    guildName = StringField(required=False, default=None)
    level = IntField(required=True)
    name = StringField(required=True)
    updated = DateTimeField(default=datetime.datetime.utcnow)
    user = StringField(required=True, default=None)
    wounds = StringField(required=False, default=None)
    x = IntField(required=False, default=None)
    y = IntField(required=False, default=None)

    # Additional fields
    race = StringField(required=False, default=None)
    img = StringField(required=False, default=None)
    dla = StringField(required=False, default=None)
    pas = IntField(required=False, default=None)
    pos = IntField(required=False, default=None)
    xp = IntField(required=False, default=None)
    xpMax = IntField(required=False, default=None)
    pv = IntField(required=False, default=None)
    pvMax = IntField(required=False, default=None)
    attM = IntField(required=False, default=None)
    defM = IntField(required=False, default=None)
    degM = IntField(required=False, default=None)
    arm = IntField(required=False, default=None)
    mmM = IntField(required=False, default=None)
    pc = IntField(required=False, default=None)

    meta = {
        'collection': 'players',
        'indexes': [],
    }
