from sqlalchemy import Integer
from sqlalchemy.sql.expression import cast

from clld.web.datatables import Values
from clld.web.datatables.base import Col, LinkCol, IntegerIdCol, DataTable, LinkToMapCol
from clld.web.datatables.contribution import Contributions, CitationCol, ContributorsCol
from clld.web.datatables import contributor
from clld.web.datatables.parameter import Parameters
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.models.common import Language, Parameter, Value

from ids.models import Chapter, Entry


class IDSCodeCol(Col):
    """special handling for IDS code
    """
    __kw__ = {'sTitle': 'IDS code'}

    def format(self, item):
        return self.get_obj(item).id.replace('-', '.')

    def order(self):
        return Entry.chapter_pk, cast(Entry.sub_code, Integer)

    def search(self, qs):
        return Entry.id.contains(qs.replace('.', '-'))


class ChapterCol(Col):
    def __init__(self, *args, **kw):
        kw['choices'] = [(sf.pk, sf.name) for sf in DBSession.query(Chapter).order_by(Chapter.pk)]
        super(ChapterCol, self).__init__(*args, **kw)

    def format(self, item):
        obj = self.get_obj(item)
        return obj.chapter.name

    def order(self):
        return Entry.chapter_pk

    def search(self, qs):
        return Entry.chapter_pk == int(qs)


class Counterparts(Values):
    """Lists of counterparts
    """
    def col_defs(self):
        if self.parameter:
            return [
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
                LinkCol(self, 'language', model_col=Language.name, get_object=lambda i: i.valueset.language),
                LinkCol(self, 'counterparts', model_col=Value.name),
                Col(self, 'description'),
            ]

        return [
            IDSCodeCol(self, 'ids_code', model_col=Parameter.id, get_object=lambda i: i.valueset.parameter),
            LinkCol(self, 'meaning', model_col=Parameter.name, get_object=lambda i: i.valueset.parameter),
            ChapterCol(self, 'chapter', get_object=lambda i: i.valueset.parameter),
            LinkCol(self, 'counterparts', model_col=Value.name),
            Col(self, 'description'),
        ]


class ContributionsCol(Col):
    __kw__ = {'bSearchable': False, 'bSortable': False}

    def format(self, item):
        return HTML.ul(
            *[HTML.li(
                link(self.dt.req, c.contribution),
                HTML.span(' (%s)' % c.jsondatadict['role'])
            ) for c in item.contribution_assocs])


class Compilers(contributor.Contributors):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            ContributionsCol(self, 'contributions'),
        ]


class Dictionaries(Contributions):
    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            LinkToMapCol(self, 'm', get_object=lambda i: i.language),
            ContributorsCol(self, 'contributor'),
            CitationCol(self, 'cite'),
        ]


class Entries(Parameters):
    __constraints__ = [Chapter]

    def base_query(self, query):
        query = query.join(Chapter)
        if self.chapter:
            query = query.filter(Chapter.pk == self.chapter.pk)
        return query

    def col_defs(self):
        return filter(lambda col: not self.chapter or col.name != 'sf', [
            IDSCodeCol(self, 'ids_code'),
            LinkCol(
                self, 'name', sTitle='Meaning',
                sDescription="This column shows the labels of the Loanword Typology "
                "meanings. By clicking on a meaning label, you get more information "
                "about the meaning, as well as a list of all words that are counterparts "
                "of that meaning."),
            ChapterCol(self, 'sf', sTitle='Chapter'),
        ])


class Chapters(DataTable):
    def col_defs(self):
        return [
            IntegerIdCol(self, 'id'),
            LinkCol(self, 'name'),
        ]


def includeme(config):
    config.register_datatable('values', Counterparts)
    #config.register_datatable('languages', WoldLanguages)
    config.register_datatable('contributors', Compilers)
    #config.register_datatable('contributions', Vocabularies)
    config.register_datatable('parameters', Entries)
    config.register_datatable('chapters', Chapters)
