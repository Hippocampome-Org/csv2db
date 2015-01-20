# fragment_string_field.py

from ..models import Article, ArticleEvidenceRel, Attachment, Evidence, EvidenceFragmentRel, Fragment
from ..models import article_not_found

# ingests morph_fragment.csv, marker_fragment.csv and populates ArticleEvidenceRel, Evidence, EvidenceFragmentRel, Fragment
class FragmentStringField:
    def parse_and_save(row,saw_protocol_reference,is_morph_fragment_csv,fragment_id):
        try:
            reference_id = int(row['ReferenceID'])
        except Exception:
            reference_id = None
        try:
            material_used = row['Material Used']
            if len(material_used) == 0:
                material_used = None
        except Exception:
            material_used = None
        try:
            location_in_reference = row['Location in reference']
            if len(location_in_reference) == 0:
                location_in_reference = None
        except Exception:
            location_in_reference = None
        try:
            protocol_reference = row['Protocol Reference']
            if len(protocol_reference) == 0:
                protocol_reference = None
        except Exception:
            protocol_reference = None
        try:
            location_in_protocol_reference = row['Location in protocol reference']
            if len(location_in_protocol_reference) == 0:
                location_in_protocol_reference = None
        except Exception:
            location_in_protocol_reference = None
        try:
            pmid_isbn = int(row['PMID/ISBN'].replace('-',''))
        except Exception:
            pmid_isbn = None
        try:
            pmid_isbn_page = int(row['pmid_isbn_page'])
        except Exception:
            pmid_isbn_page = None
        # set article_id
        if pmid_isbn == None:
            article_id = None
        else:
            row_object = None
            if pmid_isbn_page != None:
                if pmid_isbn_page == 0:
                    try:
                        row_object = Article.objects.filter(pmid_isbn=pmid_isbn).order_by('id').first()
                    except Article.DoesNotExist:
                        article_id = None
                else:
                    try:
                        row_object = Article.objects.get(pmid_isbn=pmid_isbn,first_page=pmid_isbn_page)
                    except Article.DoesNotExist:
                        article_id = None
            else:
                try:
                    row_object = Article.objects.filter(pmid_isbn=pmid_isbn).order_by('id').first()
                except Article.DoesNotExist:
                    article_id = None
            if row_object == None:
                article_id = None
            else:
                article_id = row_object.id
            if article_id == None:
                # write new pmid_isbn to article_not_found
                try:
                    row_object = article_not_found.objects.get(pmid_isbn=pmid_isbn)
                except article_not_found.DoesNotExist:
                    row_object = article_not_found(pmid_isbn=pmid_isbn)
                    row_object.save()
        #end set article_id
        type = 'data'
        obj = Attachment.objects.filter(original_id=reference_id, type='morph_figure').order_by('id').last()
        if obj is None:
            attachment      = None
            attachment_type = None
        else:
            attachment      = obj.name
            attachment_type = obj.type
        if reference_id != None:
            # Fragment type = type
            row_object = Fragment(
                original_id     = reference_id,
                quote           = material_used,
                page_location   = location_in_reference,
                pmid_isbn       = pmid_isbn,
                pmid_isbn_page  = pmid_isbn_page,
                type            = type,
                attachment      = attachment,
                attachment_type = attachment_type
            )
            row_object.save()
            row_object = Evidence()
            row_object.save()
            row_object = EvidenceFragmentRel(
                Evidence_id = fragment_id + 1,
                Fragment_id = fragment_id
            )
            row_object.save()
            row_object = ArticleEvidenceRel(
                Article_id  = article_id,
                Evidence_id = fragment_id + 1
            )
            row_object.save()
            fragment_id = fragment_id + 1
            if saw_protocol_reference == 1:
                # Fragment type = 'protocol'
                row_object = Fragment(
                    original_id     = reference_id,
                    quote           = protocol_reference,
                    page_location   = location_in_protocol_reference,
                    pmid_isbn       = pmid_isbn,
                    pmid_isbn_page  = pmid_isbn_page,
                    type            = 'protocol',
                    attachment      = attachment,
                    attachment_type = attachment_type
                )
                row_object.save()
                row_object = Evidence()
                row_object.save()
                row_object = EvidenceFragmentRel(
                    Evidence_id = fragment_id + 1,
                    Fragment_id = fragment_id
                )
                row_object.save()
                row_object = ArticleEvidenceRel(
                    Article_id  = article_id,
                    Evidence_id = fragment_id + 1
                )
                row_object.save()
                fragment_id = fragment_id + 1
                # Fragment type = 'animal'
                row_object = Fragment(
                    original_id     = reference_id,
                    quote           = None,
                    page_location   = None,
                    pmid_isbn       = None,
                    pmid_isbn_page  = None,
                    type            = 'animal',
                    attachment      = attachment,
                    attachment_type = attachment_type
                )
                row_object.save()
                row_object = Evidence()
                row_object.save()
                row_object = EvidenceFragmentRel(
                    Evidence_id = fragment_id + 1,
                    Fragment_id = fragment_id
                )
                row_object.save()
                row_object = ArticleEvidenceRel(
                    Article_id  = article_id,
                    Evidence_id = fragment_id + 1
                )
                row_object.save()
                fragment_id = fragment_id + 1
            # end if saw_protocol_reference == 1:
        #end if reference_id != None:
        return(fragment_id)
    #end def parse_and_save(row):
