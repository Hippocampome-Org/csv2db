# map.py

import codecs
import os
import re
from csv import DictReader, reader
from datetime import datetime as dt
from io import TextIOWrapper
from ..models import Article, ArticleAuthorRel, ArticleEvidenceRel, Attachment, Author, Evidence, EvidenceFragmentRel, Fragment, FragmentTypeRel, Synonym, SynonymTypeRel, Term, Type, TypeTypeRel
from ..models import article_not_found
from .epdata_string_field import EpdataPropertyRecords, EpdataStringField
from .fragment_string_field import FragmentStringField
from .markerdata_string_field import MarkerdataStringField
from .morphdata_string_field import MorphdataPropertyRecords, MorphdataStringField

class Map:

    # reads specified csv file
    def __init__(self, request):
        self.request = request
        #self.rows = DictReader(TextIOWrapper(self.request.FILES['file'].file, encoding='UTF-8'))
        self.f = TextIOWrapper(self.request.FILES['file'].file, encoding='UTF-8')
        # look for morphdata file type and associated preheader lines to skip
        saw_morphdata = 0
        lines_to_skip = 0
        self.rows = reader(self.f, delimiter=',')
        for row in self.rows:
            if row[0] == '1.0 \\alpha':
                saw_morphdata = 1
                lines_to_skip = 1
            else:
                if saw_morphdata == 1:
                    if row[0] == 'Class Status':
                        break
                    lines_to_skip = lines_to_skip + 1
                else:
                    break
        self.f.seek(0) # rewind the file
        if saw_morphdata == 1: # skip preheader lines if morphdata
            while lines_to_skip > 0:
                next(self.f) # read next line in file
                lines_to_skip = lines_to_skip - 1
        self.rows = DictReader(self.f)

    # from the command line, ingests the all.csv file and processes the contained list of files
    def all_csv(self, dev=None):
        module_dir = os.path.dirname(__file__)  # get current directory
        #example before sub: module_dir = '/Users/djh/wd/krasnow/csv2db/lib'
        module_dir = re.sub(r'csv2db/lib', r'static/csv2db/dat', module_dir)
        #example after sub : module_dir = '/Users/djh/wd/krasnow/static/csv2db/dat'
        if dev is None:
            all_csv_filename = 'all.csv'
            all_csv_file_path = os.path.join(module_dir, all_csv_filename)
            all_csv_file_buffer = open(all_csv_file_path, 'rb')
            self.rows = DictReader(TextIOWrapper(all_csv_file_buffer, encoding='UTF-8'))
            self.stdout.write('%s begin... %s' % (dt.now(), all_csv_file_path))
            Map.all_to_all(self)
            self.stdout.write('%s .....end %s' % (dt.now(), all_csv_file_path))
        elif (dev == 'false') or (dev == 'true'):
            type_csv_filename = 'type.csv'
            type_csv_file_path = os.path.join(module_dir, type_csv_filename)
            type_csv_file_buffer = open(type_csv_file_path, 'rb')
            self.rows = DictReader(TextIOWrapper(type_csv_file_buffer, encoding='UTF-8'))
            self.stdout.write('%s begin... %s' % (dt.now(), type_csv_file_path))
            Map.type_to_type(self, dev)
            self.stdout.write('%s .....end %s' % (dt.now(), type_csv_file_path))
        elif dev == 'term':
            term_csv_filename = 'term.csv'
            term_csv_file_path = os.path.join(module_dir, term_csv_filename)
            term_csv_file_buffer = open(term_csv_file_path, 'rb')
            self.rows = DictReader(TextIOWrapper(term_csv_file_buffer, encoding='UTF-8'))
            self.stdout.write('%s begin... %s' % (dt.now(), term_csv_file_path))
            Map.term_to_term(self)
            self.stdout.write('%s .....end %s' % (dt.now(), term_csv_file_path))
        else:
            pass

    # ingests the all.csv file and processes the contained list of files
    def all_to_all(self):
        process_order = []
        csv_filenames = []
        module_dir = os.path.dirname(__file__)  # get current directory
        #example before sub: module_dir = '/Users/djh/wd/krasnow/csv2db/lib'
        module_dir = re.sub(r'csv2db/lib', r'static/csv2db/dat', module_dir)
        #example after sub : module_dir = '/Users/djh/wd/krasnow/static/csv2db/dat'
        for row in self.rows:
            process_order.append(row['process order'])
            csv_filenames.append(row['csv filename'])
        for order, csv_filename in zip(process_order, csv_filenames):
            csv_file_path   = os.path.join(module_dir, csv_filename)
            csv_file_buffer = open(csv_file_path, 'rb')
            #self.rows = DictReader(TextIOWrapper(csv_file_buffer, encoding='UTF-8'))
            self.f = TextIOWrapper(csv_file_buffer, encoding='UTF-8')
            # look for morphdata file type and associated preheader lines to skip
            saw_morphdata = 0
            lines_to_skip = 0
            self.rows = reader(self.f, delimiter=',')
            for row in self.rows:
                if row[0] == '1.0 \\alpha':
                    saw_morphdata = 1
                    lines_to_skip = 1
                else:
                    if saw_morphdata == 1:
                        if row[0] == 'Class Status':
                            break
                        lines_to_skip = lines_to_skip + 1
                    else:
                        break
            self.f.seek(0) # rewind the file
            if saw_morphdata == 1: # skip preheader lines if morphdata
                while lines_to_skip > 0:
                    next(self.f) # read next line in file
                    lines_to_skip = lines_to_skip - 1
            self.rows = DictReader(self.f)
            try:
                self.stdout.write('%s begin... [%02s] %s' % (dt.now(), order, csv_file_path))
            except AttributeError:
                pass
            if   order == '1':
               #dev = 'true'
               dev = 'false'
               Map.type_to_type(self, dev)
            elif order == '2':
               Map.notes_to_type(self)
            elif order == '3':
               Map.connection_to_connection(self)
            elif order == '4':
               Map.synonym_to_synonym(self)
            elif order == '5':
               Map.article_to_article(self)
            elif order == '6':
               Map.attachment_to_attachment(self)
            elif order == '7':
               Map.attachment_to_attachment(self)
            elif order == '8':
               Map.attachment_to_attachment(self)
            elif order == '9':
               Map.fragment_to_fragment(self)
            elif order == '10':
               Map.fragment_to_fragment(self)
            elif order == '11':
               Map.fragment_to_fragment(self)
            elif order == '12':
               Map.markerdata_to_markerdata(self)
            elif order == '13':
               Map.epdata_to_epdata(self)
            elif order == '14':
               Map.morphdata_to_morphdata(self)
            else:
                pass
            try:
                self.stdout.write('%s .....end [%02s] %s' % (dt.now(), order, csv_file_path))
            except AttributeError:
                pass
            csv_file_buffer.close()

    # ingests article.csv and populates Article, ArticleAuthorRel, Author
    def article_to_article(self): # and article_to_author
        pmid_isbn_reads = []
        first_page_reads = []
        name_list = [] # authors
        article_id = 0
        for row in self.rows:
            pmid_isbn = row['pmid_isbn'].replace('-','')
            pmcid = row['pmcid']
            if len(pmcid) == 0:
                pmcid = None
            nihmsid = row['nihmsid']
            if len(nihmsid) == 0:
                nihmsid = None
            doi = row['doi']
            if len(doi) == 0:
                doi = None
            try:
                open_access = int(row['open_access'])
            except ValueError:
                open_access = None
            title = row['title']
            if len(title) == 0:
                title = None
            publication = row['publication']
            if len(publication) == 0:
                publication = None
            volume = row['volume']
            if len(volume) == 0:
                volume = None
            issue = row['issue']
            if len(issue) == 0:
                issue = None
            try:
                first_page = int(row['first_page'])
            except ValueError:
                first_page = None
            try:
                last_page = int(row['last_page'])
            except ValueError:
                last_page = None
            year = row['year']
            if len(year) == 0:
                year = None
            try:
                citation_count = int(row['citation_count'])
            except ValueError:
                citation_count = None
            row_object = Article(
                pmid_isbn      = pmid_isbn,
                pmcid          = pmcid,
                nihmsid        = nihmsid,
                doi            = doi,
                open_access    = open_access,
                title          = title,
                publication    = publication,
                volume         = volume,
                issue          = issue,
                first_page     = first_page,
                last_page      = last_page,
                year           = year,
                citation_count = citation_count
            )
            # check for dups in article.csv and only continue processing if new
            saw_article = 0
            for pmid_isbn_read, first_page_read in zip(pmid_isbn_reads, first_page_reads):
                if (pmid_isbn_read == pmid_isbn) and (first_page_read == first_page):
                    saw_article = 1
            if saw_article == 0:
                row_object.save()
                article_id = article_id + 1
                pmid_isbn_reads.append(pmid_isbn)
                first_page_reads.append(first_page)
    
                # article_to_author
                auth_string = row['authors']
                auth_list = auth_string.split(',')
                author_pos = 0
                for auth in auth_list:
                    name = auth.strip()
                    if name not in name_list:
                        row_object = Author(
                            name = name
                        )
                        row_object.save()
                        name_list.append(name)
    
                    # ArticleAuthorRel
                    row_object = ArticleAuthorRel(
                        Author_id  = name_list.index(name) + 1,
                        Article_id = article_id,
                        author_pos = author_pos
                    )
                    row_object.save()
                    author_pos = author_pos + 1
                #end for auth in auth_list:
            #end if saw_article == 0:
        # end for row in self.rows:
    #end def article_to_article(self): # and article_to_author

    # ingests attachment_morph.csv, attachment_marker.csv, attachment_ephys.csv and populates Attachment, FragmentTypeRel
    def attachment_to_attachment(self):
        is_attachment_morph_csv = 0
        for row in self.rows: # is this an attachment_morph.csv file or not
            try:
                priority = row['Representative?']
                is_attachment_morph_csv = 1
            except Exception:
                is_attachment_morph_csv = 0
            break
        self.f.seek(0) # rewind the file
        self.rows = DictReader(self.f)
        for row in self.rows:
            try:
                # set cell_identifier
                cell_identifier = int(row['Cell Identifier'])
                # set quote_reference_id
                try:
                    quote_reference_id = int(row['Quote reference id'])
                except ValueError:
                    quote_reference_id = None
                # set name_of_file_containing_figure
                name_of_file_containing_figure = row['Name of file containing figure']
                if len(name_of_file_containing_figure) == 0:
                    name_of_file_containing_figure = None
                # set figure_table
                figure_table = row['Figure/Table']
                if is_attachment_morph_csv == 1:
                    if figure_table == 'figure':
                        figure_table = 'morph_figure'
                    elif figure_table == 'table':
                        figure_table = 'morph_table'
                # set parameter
                parameter = None
                try:
                    parameter = row['Parameter'].strip()
                    if len(parameter) == 0:
                        parameter = None
                    else:
                        # map Attachment parameter value to Fragment parameter value
                        parameters_attachment = ('Vrest', 'Rin', 'tau', 'Vthresh', 'fAHP', 'APamplitude', 'APwidth', 'maxFR', 'sAHP', 'sag')
                        parameters_fragment   = ('Vrest', 'Rin', 'tau', 'Vthresh', 'fAHP', 'APampl'     , 'APwidth', 'maxFR', 'sAHP', 'sag')
                        p = 0
                        for parameter_attachment in parameters_attachment:
                            if parameter == parameter_attachment:
                                parameter = parameters_fragment[p]
                                break
                            else:
                                p = p + 1
                except Exception:
                    parameter = None
                # set interpretation_notes
                try:
                    interpretation_notes = row['Interpretation notes figures'].strip()
                    if len(interpretation_notes) == 0:
                        interpretation_notes = None
                except Exception:
                    interpretation_notes = None
                # write Attachment record
                row_object = Attachment(
                    cell_id              = cell_identifier,
                    original_id          = quote_reference_id,
                    name                 = name_of_file_containing_figure,
                    type                 = figure_table,
                    parameter            = parameter,
                    interpretation_notes = interpretation_notes
                )
                row_object.save()
                # write FragmentTypeRel row
                if is_attachment_morph_csv == 1:
                    priority = row['Representative?']
                    row_object = None
                    if priority == '1':
                        row_object = FragmentTypeRel(Type_id=cell_identifier,priority=1)
                    else:
                        row_object = FragmentTypeRel(Type_id=cell_identifier,priority=None)
                    row_object.save()
                else:
                    priority = None
            except ValueError:
                cell_identifier = None

    # ingests known_connections.csv and populates TypeTypeRel
    def connection_to_connection(self):
        for row in self.rows:
            try:
                Type1_id = int(row['Source class identity'])
                Type2_id = int(row['Target class identity'])
            except ValueError:
                continue
            connection_status_string = row['Connection?']
            connection_status = 'negative'
            if connection_status_string == '1':
               connection_status = 'positive'
            connection_location_string = row['Target layer']
            #connection_locations = connection_location_string.split(',') # was using ',' separator in original version of known_connections.csv
            connection_locations = connection_location_string.split(';') # now using ';' separator in new version of known_connections.csv
            for connection_location in connection_locations:
                try:
                    row_object = TypeTypeRel.objects.get(Type1_id=Type1_id,Type2_id=Type2_id,connection_status=connection_status,connection_location=connection_location.strip())
                except TypeTypeRel.DoesNotExist:
                    row_object = TypeTypeRel(Type1_id=Type1_id,Type2_id=Type2_id,connection_status=connection_status,connection_location=connection_location.strip())
                    row_object.save()

    # ingests epdata.csv and populates ArticleEvidenceRel, ArticleSynonymRel, Epdata, EpdataEvidenceRel, Evidence, EvidenceEvidenceRel, EvidenceFragmentRel, EvidencePropertyTypeRel, Fragment, Property
    def epdata_to_epdata(self):
        EpdataPropertyRecords.save()
        for row in self.rows:
            try:
                EpdataStringField.parse_and_save(row)
            except Exception:
                break

    # ingests morph_fragment.csv, marker_fragment.csv, ep_fragment.csv and populates ArticleEvidenceRel, Evidence, EvidenceFragmentRel, Fragment, FragmentTypeRel(updates Fragment_id field)
    def fragment_to_fragment(self):
        fragment_id = 1
        for row in self.rows: # is this a morph_fragment.csv file or a marker_fragment.csv file
            is_morph_fragment_csv          = 0
            saw_protocol_reference         = 0
            saw_ephys_parameters_extracted = 0
            try:
                protocol_reference = row['Protocol Reference']
                saw_protocol_reference = 1
                row_object  = EvidenceFragmentRel.objects.last()
                fragment_id = row_object.Fragment_id + 1 # initialize from last morph_fragment.csv entry
            except Exception:
                try:
                    ephys_parameters_extracted = row['Ephys Parameters Extracted']
                    saw_ephys_parameters_extracted = 1
                    row_object  = EvidenceFragmentRel.objects.last()
                    fragment_id = row_object.Fragment_id + 1 # initialize from last morph_fragment.csv entry
                except Exception:
                    is_morph_fragment_csv = 1
                    row_object = Evidence()
                    row_object.save()
                    fragment_id = 1
            break
        self.f.seek(0) # rewind the file
        self.rows = DictReader(self.f)
        for row in self.rows:
            fragment_id = FragmentStringField.parse_and_save(row,fragment_id,saw_protocol_reference,saw_ephys_parameters_extracted)
        #end for row in self.rows:
        # conditionally update Fragment_id fields in FragmentTypeRel
        if is_morph_fragment_csv == 1:
            FragmentTypeRel_row_objects = FragmentTypeRel.objects.all()
            for FragmentTypeRel_row_object in FragmentTypeRel_row_objects:
                try:
                    row_object  = Attachment.objects.get(id=FragmentTypeRel_row_object.id)
                    original_id = row_object.original_id
                    row_object  = Fragment.objects.get(original_id=original_id)
                    Fragment_id = row_object.id
                    row_object  = FragmentTypeRel.objects.filter(id=FragmentTypeRel_row_object.id).update(Fragment_id=Fragment_id)
                except Fragment.DoesNotExist:
                    row_object = None
        #end conditionally update Fragment_id fields in FragmentTypeRel
    #end def fragment_to_fragment(self):

    # ingests markerdata.csv and populates ArticleSynonymRel, Evidence, EvidenceEvidenceRel, EvidenceMarkerdataRel, EvidencePropertyTypeRel, Markerdata, Property
    def markerdata_to_markerdata(self):
        for row in self.rows:
            try:
                MarkerdataStringField.parse_and_save(row)
            except Exception:
                break

    # ingests morphdata.csv and populates ArticleSynonymRel, EvidencePropertyTypeRel, Property
    def morphdata_to_morphdata(self):
        MorphdataPropertyRecords.save()
        for row in self.rows:
            try:
                MorphdataStringField.parse_and_save(row)
            except Exception:
                break

    # ingests notes.csv and populates Type(updates notes field)
    def notes_to_type(self):
        module_dir        = os.path.dirname(__file__)  # get current directory
        #notes_csv         = self.request.FILES['file'].name
        #notes_csv_split   = notes_csv.split('.')
        #notes_folder_name = notes_csv_split[0]
        notes_folder_name = 'packet_notes'
        notes_folder_path = os.path.join(module_dir, notes_folder_name)
        for row in self.rows:
            unique_ID = row['unique ID']
            try:
                Type_id = int(unique_ID)
            except ValueError:
                Type_id = None
            notes_file = row['Notes file']
            if notes_file != None:
                if len(notes_file) >= len('nnnn.txt'):
                    notes_folder_path_notes_file = notes_folder_path + '/' + notes_file
                    #example before: notes_folder_path_notes_file = '/Users/djh/wd/krasnow/csv2db/lib/packet_notes/1000.txt'
                    notes_folder_path_notes_file = re.sub(r'csv2db/lib', r'static/csv2db/dat', notes_folder_path_notes_file)
                    #example after : notes_folder_path_notes_file = '/Users/djh/wd/krasnow/static/csv2db/dat/packet_notes/1000.txt'
                    try:
                        fs = codecs.open(notes_folder_path_notes_file, 'r', 'utf-8')
                        notes_txt = fs.read()
                        fs.close()
                        row_object = Type.objects.filter(id=Type_id).update(notes=notes_txt)
                    except Type.DoesNotExist:
                        row_object = None

    # ingests synonym.csv and populates Synonym, SynonymTypeRel
    def synonym_to_synonym(self):
        for row in self.rows:
            cited_names = row['Cited names']
            if len(cited_names) == 0:
                cited_names = None
            try:
                unique_id = int(row['Unique ID'])
            except ValueError:
                unique_id = None
            row_object = Synonym(
                name    = cited_names,
                cell_id = unique_id
            )
            row_object.save()
            # write SynonymTypeRel record
            Synonym_id = row_object.id
            Type_id    = row_object.cell_id
            row_object = SynonymTypeRel(Synonym_id=Synonym_id,Type_id=Type_id)
            row_object.save()

    # ingests term.csv and populates Term
    def term_to_term(self):
        for row in self.rows:
            parent = row['Parent']
            if len(parent) == 0:
                parent = None
            term = row['Term']
            if len(term) == 0:
                term = None
            portal = row['Portal']
            if len(portal) == 0:
                portal = None
            repository = row['Repository']
            if len(repository) == 0:
                repository = None
            unique_id = row['Unique ID']
            if len(unique_id) == 0:
                unique_id = None
            definition_link = row['Definition Link']
            if len(definition_link) == 0:
                definition_link = None
            row_object = Term(
                parent          = parent,
                term            = term,
                portal          = portal,
                repository      = repository,
                unique_id       = unique_id,
                definition_link = definition_link
            )
            row_object.save()

    # ingests type.csv and populates Type(all but notes field)
    def type_to_type(self, dev):
        for row in self.rows:
            status = row['status']
            if status == 'active':
                id = int(row['id'])
                try:
                    position             = int(row['position'])
                    position_HC_standard = int(row['position_HC_standard'])
                except ValueError:
                    position = None
                subregion = row['subregion']
                if len(subregion) == 0:
                    subregion = None
                full_name = row['full_name']
                if len(full_name) == 0:
                    full_name = None
                intermediate_name = row['intermediate_name']
                if len(intermediate_name) == 0:
                    intermediate_name = None
                short_name = row['short_name']
                if len(short_name) == 0:
                    short_name = None
                if dev == 'true': # overide for dev site
                    position   = position_HC_standard
                    short_name = intermediate_name
                excit_inhib = row['excit_inhib']
                notes = None
                try:
                    row_object = Type.objects.get(id=id)
                    row_object = Type.objects.filter(id=id).update(position=position,nickname=short_name)
                except Type.DoesNotExist:
                    row_object = Type(
                        id          = id,
                        position    = position,
                        subregion   = subregion,
                        name        = full_name,
                        nickname    = short_name,
                        excit_inhib = excit_inhib,
                        status      = status,
                        notes       = notes
                    )
                    row_object.save()
            #end if status == 'active':
        #end for row in self.rows:
    #end def type_to_type(self):
