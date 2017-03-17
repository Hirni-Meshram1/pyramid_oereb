
import sqlalchemy.ext.declarative
import sqlalchemy as sa

from geoalchemy2.types import Geometry
from sqlalchemy.orm import relationship

NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = sa.MetaData(naming_convention=NAMING_CONVENTION)
Base = sqlalchemy.ext.declarative.declarative_base()


class Plr73Authority(Base):
    __table_args__ = {'schema': 'plr73'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr73ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr73'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr73Authority.id), nullable=True
    )
    authority = relationship(Plr73Authority, backref='reference_definitions')


class Plr73DocumentBase(Base):
    __table_args__ = {'schema': 'plr73'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr73Document(Plr73DocumentBase):
    __table_args__ = {'schema': 'plr73'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73Authority.id),
        nullable=True
    )
    authority = relationship(Plr73Authority, backref='documents')


class Plr73Article(Plr73DocumentBase):
    __table_args__ = {'schema': 'plr73'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73Document.id),
        nullable=False
    )
    document = relationship(
        Plr73Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr73LegalProvision(Plr73Document):
    __table_args__ = {'schema': 'plr73'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr73ViewService(Base):
    __table_args__ = {'schema': 'plr73'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr73LegendEntry(Base):
    __table_args__ = {'schema': 'plr73'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr73ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr73PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr73'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr73ViewService,
        backref='public_law_restrictions'
    )


class Plr73Geometry(Base):
    __table_args__ = {'schema': 'plr73'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('LINESTRING', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73Authority.id),
        nullable=True
    )
    authority = relationship(Plr73Authority, backref='geometries')


class Plr73PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr73'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr73Authority,
        backref='public_law_restrictions'
    )


class Plr73PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr73'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73PublicLawRestriction.id),
        nullable=False
    )


class Plr73PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr73'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr73DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr73'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73Document.id),
        nullable=False
    )


class Plr73DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr73'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr73ReferenceDefinition.id),
        nullable=False
    )


class Plr87Authority(Base):
    __table_args__ = {'schema': 'plr87'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr87ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr87'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr87Authority.id), nullable=True
    )
    authority = relationship(Plr87Authority, backref='reference_definitions')


class Plr87DocumentBase(Base):
    __table_args__ = {'schema': 'plr87'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr87Document(Plr87DocumentBase):
    __table_args__ = {'schema': 'plr87'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87Authority.id),
        nullable=True
    )
    authority = relationship(Plr87Authority, backref='documents')


class Plr87Article(Plr87DocumentBase):
    __table_args__ = {'schema': 'plr87'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87Document.id),
        nullable=False
    )
    document = relationship(
        Plr87Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr87LegalProvision(Plr87Document):
    __table_args__ = {'schema': 'plr87'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr87ViewService(Base):
    __table_args__ = {'schema': 'plr87'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr87LegendEntry(Base):
    __table_args__ = {'schema': 'plr87'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr87ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr87PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr87'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr87ViewService,
        backref='public_law_restrictions'
    )


class Plr87Geometry(Base):
    __table_args__ = {'schema': 'plr87'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('LINESTRING', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87Authority.id),
        nullable=True
    )
    authority = relationship(Plr87Authority, backref='geometries')


class Plr87PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr87'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr87Authority,
        backref='public_law_restrictions'
    )


class Plr87PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr87'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87PublicLawRestriction.id),
        nullable=False
    )


class Plr87PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr87'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr87DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr87'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87Document.id),
        nullable=False
    )


class Plr87DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr87'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr87ReferenceDefinition.id),
        nullable=False
    )


class Plr88Authority(Base):
    __table_args__ = {'schema': 'plr88'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr88ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr88'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr88Authority.id), nullable=True
    )
    authority = relationship(Plr88Authority, backref='reference_definitions')


class Plr88DocumentBase(Base):
    __table_args__ = {'schema': 'plr88'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr88Document(Plr88DocumentBase):
    __table_args__ = {'schema': 'plr88'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88Authority.id),
        nullable=True
    )
    authority = relationship(Plr88Authority, backref='documents')


class Plr88Article(Plr88DocumentBase):
    __table_args__ = {'schema': 'plr88'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88Document.id),
        nullable=False
    )
    document = relationship(
        Plr88Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr88LegalProvision(Plr88Document):
    __table_args__ = {'schema': 'plr88'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr88ViewService(Base):
    __table_args__ = {'schema': 'plr88'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr88LegendEntry(Base):
    __table_args__ = {'schema': 'plr88'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr88ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr88PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr88'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr88ViewService,
        backref='public_law_restrictions'
    )


class Plr88Geometry(Base):
    __table_args__ = {'schema': 'plr88'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('LINESTRING', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88Authority.id),
        nullable=True
    )
    authority = relationship(Plr88Authority, backref='geometries')


class Plr88PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr88'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr88Authority,
        backref='public_law_restrictions'
    )


class Plr88PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr88'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88PublicLawRestriction.id),
        nullable=False
    )


class Plr88PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr88'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr88DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr88'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88Document.id),
        nullable=False
    )


class Plr88DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr88'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr88ReferenceDefinition.id),
        nullable=False
    )


class Plr97Authority(Base):
    __table_args__ = {'schema': 'plr97'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr97ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr97'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr97Authority.id), nullable=True
    )
    authority = relationship(Plr97Authority, backref='reference_definitions')


class Plr97DocumentBase(Base):
    __table_args__ = {'schema': 'plr97'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr97Document(Plr97DocumentBase):
    __table_args__ = {'schema': 'plr97'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97Authority.id),
        nullable=True
    )
    authority = relationship(Plr97Authority, backref='documents')


class Plr97Article(Plr97DocumentBase):
    __table_args__ = {'schema': 'plr97'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97Document.id),
        nullable=False
    )
    document = relationship(
        Plr97Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr97LegalProvision(Plr97Document):
    __table_args__ = {'schema': 'plr97'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr97ViewService(Base):
    __table_args__ = {'schema': 'plr97'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr97LegendEntry(Base):
    __table_args__ = {'schema': 'plr97'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr97ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr97PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr97'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr97ViewService,
        backref='public_law_restrictions'
    )


class Plr97Geometry(Base):
    __table_args__ = {'schema': 'plr97'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('LINESTRING', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97Authority.id),
        nullable=True
    )
    authority = relationship(Plr97Authority, backref='geometries')


class Plr97PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr97'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr97Authority,
        backref='public_law_restrictions'
    )


class Plr97PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr97'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97PublicLawRestriction.id),
        nullable=False
    )


class Plr97PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr97'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr97DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr97'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97Document.id),
        nullable=False
    )


class Plr97DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr97'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr97ReferenceDefinition.id),
        nullable=False
    )


class Plr96Authority(Base):
    __table_args__ = {'schema': 'plr96'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr96ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr96'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr96Authority.id), nullable=True
    )
    authority = relationship(Plr96Authority, backref='reference_definitions')


class Plr96DocumentBase(Base):
    __table_args__ = {'schema': 'plr96'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr96Document(Plr96DocumentBase):
    __table_args__ = {'schema': 'plr96'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96Authority.id),
        nullable=True
    )
    authority = relationship(Plr96Authority, backref='documents')


class Plr96Article(Plr96DocumentBase):
    __table_args__ = {'schema': 'plr96'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96Document.id),
        nullable=False
    )
    document = relationship(
        Plr96Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr96LegalProvision(Plr96Document):
    __table_args__ = {'schema': 'plr96'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr96ViewService(Base):
    __table_args__ = {'schema': 'plr96'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr96LegendEntry(Base):
    __table_args__ = {'schema': 'plr96'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr96ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr96PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr96'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr96ViewService,
        backref='public_law_restrictions'
    )


class Plr96Geometry(Base):
    __table_args__ = {'schema': 'plr96'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96Authority.id),
        nullable=True
    )
    authority = relationship(Plr96Authority, backref='geometries')


class Plr96PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr96'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr96Authority,
        backref='public_law_restrictions'
    )


class Plr96PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr96'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96PublicLawRestriction.id),
        nullable=False
    )


class Plr96PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr96'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr96DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr96'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96Document.id),
        nullable=False
    )


class Plr96DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr96'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr96ReferenceDefinition.id),
        nullable=False
    )


class Plr103Authority(Base):
    __table_args__ = {'schema': 'plr103'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr103ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr103'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr103Authority.id), nullable=True
    )
    authority = relationship(Plr103Authority, backref='reference_definitions')


class Plr103DocumentBase(Base):
    __table_args__ = {'schema': 'plr103'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr103Document(Plr103DocumentBase):
    __table_args__ = {'schema': 'plr103'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103Authority.id),
        nullable=True
    )
    authority = relationship(Plr103Authority, backref='documents')


class Plr103Article(Plr103DocumentBase):
    __table_args__ = {'schema': 'plr103'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103Document.id),
        nullable=False
    )
    document = relationship(
        Plr103Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr103LegalProvision(Plr103Document):
    __table_args__ = {'schema': 'plr103'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr103ViewService(Base):
    __table_args__ = {'schema': 'plr103'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr103LegendEntry(Base):
    __table_args__ = {'schema': 'plr103'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr103ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr103PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr103'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr103ViewService,
        backref='public_law_restrictions'
    )


class Plr103Geometry(Base):
    __table_args__ = {'schema': 'plr103'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103Authority.id),
        nullable=True
    )
    authority = relationship(Plr103Authority, backref='geometries')


class Plr103PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr103'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr103Authority,
        backref='public_law_restrictions'
    )


class Plr103PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr103'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103PublicLawRestriction.id),
        nullable=False
    )


class Plr103PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr103'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr103DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr103'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103Document.id),
        nullable=False
    )


class Plr103DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr103'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr103ReferenceDefinition.id),
        nullable=False
    )


class Plr104Authority(Base):
    __table_args__ = {'schema': 'plr104'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr104ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr104'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr104Authority.id), nullable=True
    )
    authority = relationship(Plr104Authority, backref='reference_definitions')


class Plr104DocumentBase(Base):
    __table_args__ = {'schema': 'plr104'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr104Document(Plr104DocumentBase):
    __table_args__ = {'schema': 'plr104'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104Authority.id),
        nullable=True
    )
    authority = relationship(Plr104Authority, backref='documents')


class Plr104Article(Plr104DocumentBase):
    __table_args__ = {'schema': 'plr104'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104Document.id),
        nullable=False
    )
    document = relationship(
        Plr104Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr104LegalProvision(Plr104Document):
    __table_args__ = {'schema': 'plr104'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr104ViewService(Base):
    __table_args__ = {'schema': 'plr104'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr104LegendEntry(Base):
    __table_args__ = {'schema': 'plr104'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr104ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr104PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr104'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr104ViewService,
        backref='public_law_restrictions'
    )


class Plr104Geometry(Base):
    __table_args__ = {'schema': 'plr104'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104Authority.id),
        nullable=True
    )
    authority = relationship(Plr104Authority, backref='geometries')


class Plr104PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr104'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr104Authority,
        backref='public_law_restrictions'
    )


class Plr104PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr104'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104PublicLawRestriction.id),
        nullable=False
    )


class Plr104PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr104'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr104DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr104'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104Document.id),
        nullable=False
    )


class Plr104DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr104'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr104ReferenceDefinition.id),
        nullable=False
    )


class Plr108Authority(Base):
    __table_args__ = {'schema': 'plr108'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr108ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr108'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr108Authority.id), nullable=True
    )
    authority = relationship(Plr108Authority, backref='reference_definitions')


class Plr108DocumentBase(Base):
    __table_args__ = {'schema': 'plr108'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr108Document(Plr108DocumentBase):
    __table_args__ = {'schema': 'plr108'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108Authority.id),
        nullable=True
    )
    authority = relationship(Plr108Authority, backref='documents')


class Plr108Article(Plr108DocumentBase):
    __table_args__ = {'schema': 'plr108'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108Document.id),
        nullable=False
    )
    document = relationship(
        Plr108Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr108LegalProvision(Plr108Document):
    __table_args__ = {'schema': 'plr108'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr108ViewService(Base):
    __table_args__ = {'schema': 'plr108'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr108LegendEntry(Base):
    __table_args__ = {'schema': 'plr108'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr108ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr108PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr108'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr108ViewService,
        backref='public_law_restrictions'
    )


class Plr108Geometry(Base):
    __table_args__ = {'schema': 'plr108'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108Authority.id),
        nullable=True
    )
    authority = relationship(Plr108Authority, backref='geometries')


class Plr108PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr108'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr108Authority,
        backref='public_law_restrictions'
    )


class Plr108PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr108'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108PublicLawRestriction.id),
        nullable=False
    )


class Plr108PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr108'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr108DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr108'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108Document.id),
        nullable=False
    )


class Plr108DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr108'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr108ReferenceDefinition.id),
        nullable=False
    )


class Plr116Authority(Base):
    __table_args__ = {'schema': 'plr116'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr116ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr116'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr116Authority.id), nullable=True
    )
    authority = relationship(Plr116Authority, backref='reference_definitions')


class Plr116DocumentBase(Base):
    __table_args__ = {'schema': 'plr116'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr116Document(Plr116DocumentBase):
    __table_args__ = {'schema': 'plr116'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116Authority.id),
        nullable=True
    )
    authority = relationship(Plr116Authority, backref='documents')


class Plr116Article(Plr116DocumentBase):
    __table_args__ = {'schema': 'plr116'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116Document.id),
        nullable=False
    )
    document = relationship(
        Plr116Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr116LegalProvision(Plr116Document):
    __table_args__ = {'schema': 'plr116'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr116ViewService(Base):
    __table_args__ = {'schema': 'plr116'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr116LegendEntry(Base):
    __table_args__ = {'schema': 'plr116'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr116ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr116PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr116'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr116ViewService,
        backref='public_law_restrictions'
    )


class Plr116Geometry(Base):
    __table_args__ = {'schema': 'plr116'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116Authority.id),
        nullable=True
    )
    authority = relationship(Plr116Authority, backref='geometries')


class Plr116PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr116'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr116Authority,
        backref='public_law_restrictions'
    )


class Plr116PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr116'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116PublicLawRestriction.id),
        nullable=False
    )


class Plr116PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr116'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr116DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr116'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116Document.id),
        nullable=False
    )


class Plr116DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr116'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr116ReferenceDefinition.id),
        nullable=False
    )


class Plr117Authority(Base):
    __table_args__ = {'schema': 'plr117'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr117ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr117'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr117Authority.id), nullable=True
    )
    authority = relationship(Plr117Authority, backref='reference_definitions')


class Plr117DocumentBase(Base):
    __table_args__ = {'schema': 'plr117'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr117Document(Plr117DocumentBase):
    __table_args__ = {'schema': 'plr117'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117Authority.id),
        nullable=True
    )
    authority = relationship(Plr117Authority, backref='documents')


class Plr117Article(Plr117DocumentBase):
    __table_args__ = {'schema': 'plr117'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117Document.id),
        nullable=False
    )
    document = relationship(
        Plr117Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr117LegalProvision(Plr117Document):
    __table_args__ = {'schema': 'plr117'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr117ViewService(Base):
    __table_args__ = {'schema': 'plr117'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr117LegendEntry(Base):
    __table_args__ = {'schema': 'plr117'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr117ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr117PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr117'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr117ViewService,
        backref='public_law_restrictions'
    )


class Plr117Geometry(Base):
    __table_args__ = {'schema': 'plr117'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117Authority.id),
        nullable=True
    )
    authority = relationship(Plr117Authority, backref='geometries')


class Plr117PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr117'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr117Authority,
        backref='public_law_restrictions'
    )


class Plr117PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr117'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117PublicLawRestriction.id),
        nullable=False
    )


class Plr117PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr117'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr117DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr117'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117Document.id),
        nullable=False
    )


class Plr117DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr117'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr117ReferenceDefinition.id),
        nullable=False
    )


class Plr118Authority(Base):
    __table_args__ = {'schema': 'plr118'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr118ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr118'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr118Authority.id), nullable=True
    )
    authority = relationship(Plr118Authority, backref='reference_definitions')


class Plr118DocumentBase(Base):
    __table_args__ = {'schema': 'plr118'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr118Document(Plr118DocumentBase):
    __table_args__ = {'schema': 'plr118'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118Authority.id),
        nullable=True
    )
    authority = relationship(Plr118Authority, backref='documents')


class Plr118Article(Plr118DocumentBase):
    __table_args__ = {'schema': 'plr118'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118Document.id),
        nullable=False
    )
    document = relationship(
        Plr118Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr118LegalProvision(Plr118Document):
    __table_args__ = {'schema': 'plr118'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr118ViewService(Base):
    __table_args__ = {'schema': 'plr118'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr118LegendEntry(Base):
    __table_args__ = {'schema': 'plr118'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr118ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr118PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr118'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr118ViewService,
        backref='public_law_restrictions'
    )


class Plr118Geometry(Base):
    __table_args__ = {'schema': 'plr118'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118Authority.id),
        nullable=True
    )
    authority = relationship(Plr118Authority, backref='geometries')


class Plr118PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr118'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr118Authority,
        backref='public_law_restrictions'
    )


class Plr118PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr118'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118PublicLawRestriction.id),
        nullable=False
    )


class Plr118PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr118'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr118DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr118'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118Document.id),
        nullable=False
    )


class Plr118DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr118'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr118ReferenceDefinition.id),
        nullable=False
    )


class Plr119Authority(Base):
    __table_args__ = {'schema': 'plr119'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr119ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr119'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr119Authority.id), nullable=True
    )
    authority = relationship(Plr119Authority, backref='reference_definitions')


class Plr119DocumentBase(Base):
    __table_args__ = {'schema': 'plr119'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr119Document(Plr119DocumentBase):
    __table_args__ = {'schema': 'plr119'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119Authority.id),
        nullable=True
    )
    authority = relationship(Plr119Authority, backref='documents')


class Plr119Article(Plr119DocumentBase):
    __table_args__ = {'schema': 'plr119'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119Document.id),
        nullable=False
    )
    document = relationship(
        Plr119Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr119LegalProvision(Plr119Document):
    __table_args__ = {'schema': 'plr119'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr119ViewService(Base):
    __table_args__ = {'schema': 'plr119'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr119LegendEntry(Base):
    __table_args__ = {'schema': 'plr119'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr119ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr119PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr119'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr119ViewService,
        backref='public_law_restrictions'
    )


class Plr119Geometry(Base):
    __table_args__ = {'schema': 'plr119'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119Authority.id),
        nullable=True
    )
    authority = relationship(Plr119Authority, backref='geometries')


class Plr119PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr119'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr119Authority,
        backref='public_law_restrictions'
    )


class Plr119PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr119'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119PublicLawRestriction.id),
        nullable=False
    )


class Plr119PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr119'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr119DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr119'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119Document.id),
        nullable=False
    )


class Plr119DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr119'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr119ReferenceDefinition.id),
        nullable=False
    )


class Plr131Authority(Base):
    __table_args__ = {'schema': 'plr131'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr131ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr131'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr131Authority.id), nullable=True
    )
    authority = relationship(Plr131Authority, backref='reference_definitions')


class Plr131DocumentBase(Base):
    __table_args__ = {'schema': 'plr131'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr131Document(Plr131DocumentBase):
    __table_args__ = {'schema': 'plr131'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131Authority.id),
        nullable=True
    )
    authority = relationship(Plr131Authority, backref='documents')


class Plr131Article(Plr131DocumentBase):
    __table_args__ = {'schema': 'plr131'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131Document.id),
        nullable=False
    )
    document = relationship(
        Plr131Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr131LegalProvision(Plr131Document):
    __table_args__ = {'schema': 'plr131'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr131ViewService(Base):
    __table_args__ = {'schema': 'plr131'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr131LegendEntry(Base):
    __table_args__ = {'schema': 'plr131'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr131ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr131PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr131'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr131ViewService,
        backref='public_law_restrictions'
    )


class Plr131Geometry(Base):
    __table_args__ = {'schema': 'plr131'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131Authority.id),
        nullable=True
    )
    authority = relationship(Plr131Authority, backref='geometries')


class Plr131PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr131'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr131Authority,
        backref='public_law_restrictions'
    )


class Plr131PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr131'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131PublicLawRestriction.id),
        nullable=False
    )


class Plr131PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr131'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr131DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr131'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131Document.id),
        nullable=False
    )


class Plr131DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr131'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr131ReferenceDefinition.id),
        nullable=False
    )


class Plr132Authority(Base):
    __table_args__ = {'schema': 'plr132'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr132ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr132'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr132Authority.id), nullable=True
    )
    authority = relationship(Plr132Authority, backref='reference_definitions')


class Plr132DocumentBase(Base):
    __table_args__ = {'schema': 'plr132'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr132Document(Plr132DocumentBase):
    __table_args__ = {'schema': 'plr132'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132Authority.id),
        nullable=True
    )
    authority = relationship(Plr132Authority, backref='documents')


class Plr132Article(Plr132DocumentBase):
    __table_args__ = {'schema': 'plr132'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132Document.id),
        nullable=False
    )
    document = relationship(
        Plr132Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr132LegalProvision(Plr132Document):
    __table_args__ = {'schema': 'plr132'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr132ViewService(Base):
    __table_args__ = {'schema': 'plr132'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr132LegendEntry(Base):
    __table_args__ = {'schema': 'plr132'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr132ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr132PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr132'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr132ViewService,
        backref='public_law_restrictions'
    )


class Plr132Geometry(Base):
    __table_args__ = {'schema': 'plr132'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132Authority.id),
        nullable=True
    )
    authority = relationship(Plr132Authority, backref='geometries')


class Plr132PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr132'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr132Authority,
        backref='public_law_restrictions'
    )


class Plr132PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr132'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132PublicLawRestriction.id),
        nullable=False
    )


class Plr132PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr132'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr132DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr132'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132Document.id),
        nullable=False
    )


class Plr132DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr132'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr132ReferenceDefinition.id),
        nullable=False
    )


class Plr145Authority(Base):
    __table_args__ = {'schema': 'plr145'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr145ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr145'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr145Authority.id), nullable=True
    )
    authority = relationship(Plr145Authority, backref='reference_definitions')


class Plr145DocumentBase(Base):
    __table_args__ = {'schema': 'plr145'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr145Document(Plr145DocumentBase):
    __table_args__ = {'schema': 'plr145'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145Authority.id),
        nullable=True
    )
    authority = relationship(Plr145Authority, backref='documents')


class Plr145Article(Plr145DocumentBase):
    __table_args__ = {'schema': 'plr145'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145Document.id),
        nullable=False
    )
    document = relationship(
        Plr145Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr145LegalProvision(Plr145Document):
    __table_args__ = {'schema': 'plr145'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr145ViewService(Base):
    __table_args__ = {'schema': 'plr145'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr145LegendEntry(Base):
    __table_args__ = {'schema': 'plr145'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr145ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr145PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr145'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr145ViewService,
        backref='public_law_restrictions'
    )


class Plr145Geometry(Base):
    __table_args__ = {'schema': 'plr145'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145Authority.id),
        nullable=True
    )
    authority = relationship(Plr145Authority, backref='geometries')


class Plr145PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr145'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr145Authority,
        backref='public_law_restrictions'
    )


class Plr145PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr145'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145PublicLawRestriction.id),
        nullable=False
    )


class Plr145PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr145'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr145DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr145'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145Document.id),
        nullable=False
    )


class Plr145DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr145'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr145ReferenceDefinition.id),
        nullable=False
    )


class Plr157Authority(Base):
    __table_args__ = {'schema': 'plr157'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr157ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr157'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr157Authority.id), nullable=True
    )
    authority = relationship(Plr157Authority, backref='reference_definitions')


class Plr157DocumentBase(Base):
    __table_args__ = {'schema': 'plr157'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr157Document(Plr157DocumentBase):
    __table_args__ = {'schema': 'plr157'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157Authority.id),
        nullable=True
    )
    authority = relationship(Plr157Authority, backref='documents')


class Plr157Article(Plr157DocumentBase):
    __table_args__ = {'schema': 'plr157'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157Document.id),
        nullable=False
    )
    document = relationship(
        Plr157Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr157LegalProvision(Plr157Document):
    __table_args__ = {'schema': 'plr157'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr157ViewService(Base):
    __table_args__ = {'schema': 'plr157'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr157LegendEntry(Base):
    __table_args__ = {'schema': 'plr157'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr157ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr157PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr157'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr157ViewService,
        backref='public_law_restrictions'
    )


class Plr157Geometry(Base):
    __table_args__ = {'schema': 'plr157'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157Authority.id),
        nullable=True
    )
    authority = relationship(Plr157Authority, backref='geometries')


class Plr157PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr157'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr157Authority,
        backref='public_law_restrictions'
    )


class Plr157PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr157'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157PublicLawRestriction.id),
        nullable=False
    )


class Plr157PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr157'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr157DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr157'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157Document.id),
        nullable=False
    )


class Plr157DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr157'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr157ReferenceDefinition.id),
        nullable=False
    )


class Plr159Authority(Base):
    __table_args__ = {'schema': 'plr159'}
    __tablename__ = 'authority'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    authority_web = sa.Column(sa.String, nullable=True)
    uid = sa.Column(sa.String(12), nullable=True)


class Plr159ReferenceDefinition(Base):  # TODO: Check translation
    __table_args__ = {'schema': 'plr159'}
    __tablename__ = 'reference_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    topic = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    authority_id = sa.Column(sa.Integer, sa.ForeignKey(
        Plr159Authority.id), nullable=True
    )
    authority = relationship(Plr159Authority, backref='reference_definitions')


class Plr159DocumentBase(Base):
    __table_args__ = {'schema': 'plr159'}
    __tablename__ = 'document_base'
    id = sa.Column(sa.Integer, primary_key=True)
    text_web = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    type = sa.Column(sa.Unicode, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'document_base',
        'polymorphic_on': type,
        'passive_updates': True
    }


class Plr159Document(Plr159DocumentBase):
    __table_args__ = {'schema': 'plr159'}
    __tablename__ = 'document'
    title = sa.Column(sa.String, nullable=False)
    official_title = sa.Column(sa.String, nullable=True)
    abbreviation = sa.Column(sa.String, nullable=True)
    official_number = sa.Column(sa.String, nullable=True)
    canton = sa.Column(sa.String(2), nullable=True)
    municipality = sa.Column(sa.Integer, nullable=True)
    file = sa.Column(sa.Binary, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="document")
    __mapper_args__ = {
        'polymorphic_identity': 'document'
    }
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159Authority.id),
        nullable=True
    )
    authority = relationship(Plr159Authority, backref='documents')


class Plr159Article(Plr159DocumentBase):
    __table_args__ = {'schema': 'plr159'}
    __tablename__ = 'article'
    number = sa.Column(sa.String, nullable=False)
    text = sa.Column(sa.String, nullable=True)
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159DocumentBase.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="article")
    __mapper_args__ = {
        'polymorphic_identity': 'article'
    }
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159Document.id),
        nullable=False
    )
    document = relationship(
        Plr159Document,
        backref='articles',
        foreign_keys=[document_id]
    )


class Plr159LegalProvision(Plr159Document):
    __table_args__ = {'schema': 'plr159'}
    __tablename__ = 'legal_provision'
    id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159Document.id),
        primary_key=True,
        onupdate="cascade"
    )
    type = sa.Column(sa.Unicode, nullable=True, server_default="legal_provision")
    __mapper_args__ = {
        'polymorphic_identity': 'legal_provision'
    }


class Plr159ViewService(Base):
    __table_args__ = {'schema': 'plr159'}
    __tablename__ = 'view_service'
    id = sa.Column(sa.Integer, primary_key=True)
    link_wms = sa.Column(sa.String, nullable=False)
    legend_web = sa.Column(sa.String, nullable=True)


class Plr159LegendEntry(Base):
    __table_args__ = {'schema': 'plr159'}
    __tablename__ = 'legend_entry'
    id = sa.Column(sa.Integer, primary_key=True)
    file = sa.Column(sa.Binary, nullable=False)
    legend_text = sa.Column(sa.String, nullable=False)
    type_code = sa.Column(sa.String(40), nullable=False)
    type_code_list = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159ViewService.id),
        nullable=False
    )
    view_service = relationship(Plr159ViewService, backref='legends')


# TODO: check how the definition in base model from confederation can be realized
class Plr159PublicLawRestriction(Base):
    __table_args__ = {'schema': 'plr159'}
    __tablename__ = 'public_law_restriction'
    id = sa.Column(sa.Integer, primary_key=True)
    content = sa.Column(sa.String, nullable=False)
    topic = sa.Column(sa.String, nullable=False)
    subtopic = sa.Column(sa.String, nullable=True)
    additional_topic = sa.Column(sa.String, nullable=True)
    type_code = sa.Column(sa.String(40), nullable=True)
    type_code_list = sa.Column(sa.String, nullable=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    view_service_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159ViewService.id),
        nullable=True
    )
    view_service = relationship(
        Plr159ViewService,
        backref='public_law_restrictions'
    )


class Plr159Geometry(Base):
    __table_args__ = {'schema': 'plr159'}
    __tablename__ = 'geometry'
    id = sa.Column(sa.Integer, primary_key=True)
    legal_state = sa.Column(sa.String, nullable=False)
    published_from = sa.Column(sa.Date, nullable=False)
    geo_metadata = sa.Column(sa.String, nullable=True)  # TODO: Check translation
    geom = sa.Column(Geometry('POLYGON', srid=2056))
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159Authority.id),
        nullable=True
    )
    authority = relationship(Plr159Authority, backref='geometries')


class Plr159PublicLawRestrictionBase(Base):
    __tablename__ = 'public_law_restriction_base'
    __table_args__ = {'schema': 'plr159'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159PublicLawRestriction.id),
        nullable=False
    )
    authority_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159Authority.id),
        nullable=True
    )
    authority = relationship(
        Plr159Authority,
        backref='public_law_restrictions'
    )


class Plr159PublicLawRestrictionRefinement(Base):
    __tablename__ = 'public_law_restriction_refinement'
    __table_args__ = {'schema': 'plr159'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159PublicLawRestriction.id),
        nullable=False
    )
    public_law_restriction_base_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159PublicLawRestriction.id),
        nullable=False
    )


class Plr159PublicLawRestrictionDocument(Base):
    __tablename__ = 'public_law_restriction_document'
    __table_args__ = {'schema': 'plr159'}
    id = sa.Column(sa.Integer, primary_key=True)
    public_law_restriction_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159PublicLawRestriction.id),
        nullable=False
    )
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159DocumentBase.id),
        nullable=False
    )


# TODO: check translation
class Plr159DocumentHint(Base):
    __tablename__ = 'document_hint'
    __table_args__ = {'schema': 'plr159'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159Document.id),
        nullable=False
    )
    hint_document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159Document.id),
        nullable=False
    )


class Plr159DocumentReferenceDefinition(Base):
    __tablename__ = 'document_reference_definition'
    __table_args__ = {'schema': 'plr159'}
    id = sa.Column(sa.Integer, primary_key=True)
    document_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159Document.id),
        nullable=False
    )
    reference_definition_id = sa.Column(
        sa.Integer,
        sa.ForeignKey(Plr159ReferenceDefinition.id),
        nullable=False
    )
