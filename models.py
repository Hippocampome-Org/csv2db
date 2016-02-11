from django.db import models

class FloatFloatField(models.Field): 
    def db_type(self, connection):
        return 'float'

class EnumField(models.Field):
    def __init__(self, *args, **kwargs):
        super(EnumField, self).__init__(*args, **kwargs)
        assert self.choices, "Need choices for enumeration"

    def db_type(self, connection):
        if not all(isinstance(col, str) for col, _ in self.choices):
            raise ValueError("MySQL ENUM values should be strings")
        return "ENUM({})".format(','.join("'{}'".format(col) for col, _ in self.choices))

class EnumAttachmentType(EnumField, models.CharField):
    def __init__(self, *args, choices=[], **kwargs):
        values = [('ephys_figure',  'Ephys_figure'),  ('ephys_table',  'Ephys_table'),
                  ('marker_figure', 'Marker_figure'), ('marker_table', 'Marker_table'),
                  ('morph_figure',  'Morph_figure'),  ('morph_table',  'Morph_table')]
        super(EnumAttachmentType, self).__init__(*args, choices=values, **kwargs)

class EnumEvidenceEvidenceType(EnumField, models.CharField):
    def __init__(self, *args, choices=[], **kwargs):
        values = [('interpretation', 'Interpretation'), ('inference', 'Inference')]
        super(EnumEvidenceEvidenceType, self).__init__(*args, choices=values, **kwargs)

class EnumFragmentAttachmentType(EnumField, models.CharField):
    def __init__(self, *args, choices=[], **kwargs):
        values = [('morph_figure', 'Morph_figure'), ('morph_table', 'Morph_table')]
        super(EnumFragmentAttachmentType, self).__init__(*args, choices=values, **kwargs)

class EnumFragmentType(EnumField, models.CharField):
    def __init__(self, *args, choices=[], **kwargs):
        values = [('data', 'Data'), ('protocol', 'Protocol'), ('animal', 'Animal')]
        super(EnumFragmentType, self).__init__(*args, choices=values, **kwargs)

class EnumTypeExcitInhib(EnumField, models.CharField):
    def __init__(self, *args, choices=[], **kwargs):
        values = [('e', 'E'), ('i', 'I')]
        super(EnumTypeExcitInhib, self).__init__(*args, choices=values, **kwargs)

class EnumTypeStatus(EnumField, models.CharField):
    def __init__(self, *args, choices=[], **kwargs):
        values = [('active', 'Active'), ('frozen', 'Frozen')]
        super(EnumTypeStatus, self).__init__(*args, choices=values, **kwargs)

class EnumTypeTypeConnectionStatus(EnumField, models.CharField):
    def __init__(self, *args, choices=[], **kwargs):
        values = [('positive', 'Positive'), ('negative', 'Negative')]
        super(EnumTypeTypeConnectionStatus, self).__init__(*args, choices=values, **kwargs)

class Article(models.Model):
    id             = models.AutoField(primary_key=True)
    pmid_isbn      = models.BigIntegerField(null=True)
    pmcid          = models.CharField(max_length=16, null=True)
    nihmsid        = models.CharField(max_length=16, null=True)
    doi            = models.CharField(max_length=640, null=True)
    open_access    = models.NullBooleanField(null=True)
    dt             = models.DateTimeField(auto_now_add=True)
    title          = models.CharField(max_length=512, null=True)
    publication    = models.CharField(max_length=128, null=True)
    volume         = models.CharField(max_length=15, null=True)
    issue          = models.CharField(max_length=15, null=True)
    first_page     = models.IntegerField(null=True)
    last_page      = models.IntegerField(null=True)
    year           = models.CharField(max_length=15, null=True)
    citation_count = models.IntegerField(null=True)
    class Meta:
        db_table = 'Article'

class article_not_found(models.Model):
    id        = models.AutoField(primary_key=True)
    dt        = models.DateTimeField(auto_now_add=True)
    pmid_isbn = models.BigIntegerField(null=True)
    class Meta:
        db_table = 'article_not_found'

class ArticleAuthorRel(models.Model):
    id         = models.AutoField(primary_key=True)
    dt         = models.DateTimeField(auto_now_add=True)
    Author_id  = models.IntegerField(db_index=True, unique=False, null=True)
    Article_id = models.IntegerField(db_index=True, unique=False, null=True)
    author_pos = models.IntegerField(null=True)
    class Meta:
        db_table = 'ArticleAuthorRel'

class ArticleEvidenceRel(models.Model):
    id          = models.AutoField(primary_key=True)
    dt          = models.DateTimeField(auto_now_add=True)
    Article_id  = models.IntegerField(db_index=True, unique=False, null=True)
    Evidence_id = models.IntegerField(db_index=True, unique=False, null=True)
    class Meta:
        db_table = 'ArticleEvidenceRel'

class ArticleSynonymRel(models.Model):
    id         = models.AutoField(primary_key=True)
    dt         = models.DateTimeField(auto_now_add=True)
    Article_id = models.IntegerField(db_index=True, unique=False, null=True)
    Synonym_id = models.IntegerField(db_index=True, unique=False, null=True)
    class Meta:
        db_table = 'ArticleSynonymRel'

class Attachment(models.Model):
    id                   = models.AutoField(primary_key=True)
    dt                   = models.DateTimeField(auto_now_add=True)
    cell_id              = models.IntegerField(null=True)
    original_id          = models.BigIntegerField(null=True)
    name                 = models.CharField(max_length=256, null=True)
    type                 = EnumAttachmentType(max_length=13, null=True) # enum('ephys_figure','ephys_table','marker_figure','marker_table','morph_figure','morph_table')
    parameter            = models.CharField(max_length=64, null=True)
    protocol_tag         = models.CharField(max_length=64, null=True)
    interpretation_notes = models.TextField(null=True)
    class Meta:
        db_table = 'Attachment'

class Author(models.Model):
    id   = models.AutoField(primary_key=True)
    dt   = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=64, null=True)
    class Meta:
        db_table = 'Author'

class Conndata(models.Model):
    id                  = models.AutoField(primary_key=True)
    dt                  = models.DateTimeField(auto_now_add=True)
    Type1_id            = models.IntegerField(db_index=True, unique=False, null=True)
    Type2_id            = models.IntegerField(db_index=True, unique=False, null=True)
    connection_status   = EnumTypeTypeConnectionStatus(max_length=8, null=True) # enum('positive','negative')
    connection_location = models.CharField(max_length=16, null=True)
    class Meta:
        db_table = 'Conndata'

class ConnFragment(models.Model):
    id                     = models.AutoField(primary_key=True)
    original_id            = models.BigIntegerField(null=True)
    dt                     = models.DateTimeField(auto_now_add=True)
    quote                  = models.TextField(null=True)
    page_location          = models.CharField(max_length=64, null=True)
    pmid_isbn              = models.BigIntegerField(null=True)
    class Meta:
        db_table = 'ConnFragment'

class ConndataFragmentRel(models.Model):
    id                          = models.AutoField(primary_key=True)
    dt                          = models.DateTimeField(auto_now_add=True)
    Conndata_id                 = models.IntegerField(db_index=True, unique=False, null=True)
    ConnFragment_id             = models.IntegerField(db_index=True, unique=False, null=True)
    class Meta:
        db_table = 'ConndataFragmentRel'

class Epdata(models.Model):
    id        = models.AutoField(primary_key=True)
    dt        = models.DateTimeField(auto_now_add=True)
    raw       = models.CharField(max_length=162, null=True)
    value1    = FloatFloatField(null=True)
    value2    = FloatFloatField(null=True)
    error     = FloatFloatField(null=True)
    std_sem   = models.CharField(max_length=32, null=True)
    n         = FloatFloatField(null=True)
    istim     = models.CharField(max_length=32, null=True)
    time      = models.CharField(max_length=32, null=True)
    unit      = models.CharField(max_length=8, null=True)
    location  = models.CharField(max_length=128, null=True)
    rep_value = models.CharField(max_length=128, null=True)
    gt_value  = models.NullBooleanField(null=True)
    class Meta:
        db_table = 'Epdata'

class EpdataEvidenceRel(models.Model):
    id          = models.AutoField(primary_key=True)
    dt          = models.DateTimeField(auto_now_add=True)
    Epdata_id   = models.IntegerField(db_index=True, unique=False, null=True)
    Evidence_id = models.IntegerField(db_index=True, unique=False, null=True)
    class Meta:
        db_table = 'EpdataEvidenceRel'

class Evidence(models.Model):
    id = models.AutoField(primary_key=True)
    dt = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Evidence'

class EvidenceEvidenceRel(models.Model):
    id           = models.AutoField(primary_key=True)
    dt           = models.DateTimeField(auto_now_add=True)
    Evidence1_id = models.IntegerField(db_index=True, unique=False, null=True)
    Evidence2_id = models.IntegerField(db_index=True, unique=False, null=True)
    type         = EnumEvidenceEvidenceType(max_length=14, null=True) # enum('interpretation','inference')
    class Meta:
        db_table = 'EvidenceEvidenceRel'

class EvidenceFragmentRel(models.Model):
    id          = models.AutoField(primary_key=True)
    dt          = models.DateTimeField(auto_now_add=True)
    Evidence_id = models.IntegerField(db_index=True, unique=False, null=True)
    Fragment_id = models.IntegerField(db_index=True, unique=False, null=True)
    class Meta:
        db_table = 'EvidenceFragmentRel'

class EvidenceMarkerdataRel(models.Model):
    id            = models.AutoField(primary_key=True)
    dt            = models.DateTimeField(auto_now_add=True)
    Evidence_id   = models.IntegerField(db_index=True, unique=False, null=True)
    Markerdata_id = models.IntegerField(db_index=True, unique=False, null=True)
    class Meta:
        db_table = 'EvidenceMarkerdataRel'

class EvidencePropertyTypeRel(models.Model):
    id                        = models.AutoField(primary_key=True)
    dt                        = models.DateTimeField(auto_now_add=True)
    Evidence_id               = models.IntegerField(db_index=True, unique=False, null=True)
    Property_id               = models.IntegerField(db_index=True, unique=False, null=True)
    Type_id                   = models.IntegerField(db_index=True, unique=False, null=True)
    Article_id                = models.IntegerField(db_index=True, unique=False, null=True)
    priority                  = models.IntegerField(null=True)
    conflict_note             = models.CharField(max_length=64, null=True)
    unvetted                  = models.NullBooleanField(null=True)
    linking_quote             = models.TextField(null=True)
    interpretation_notes      = models.TextField(null=True)
    property_type_explanation = models.TextField(null=True)
    soma_pcl_flag             = models.NullBooleanField(null=True)
    ax_de_pcl_flag            = models.IntegerField(unique=False,null=True)
    perisomatic_targeting_flag= models.IntegerField(unique=False,null=True)
    supplemental_pmids        = models.CharField(max_length=256, null=True)
    class Meta:
        db_table = 'EvidencePropertyTypeRel'

class Fragment(models.Model):
    id                     = models.AutoField(primary_key=True)
    original_id            = models.BigIntegerField(null=True)
    dt                     = models.DateTimeField(auto_now_add=True)
    quote                  = models.TextField(null=True)
    page_location          = models.CharField(max_length=64, null=True)
    pmid_isbn              = models.BigIntegerField(null=True)
    pmid_isbn_page         = models.IntegerField(null=True)
    type                   = EnumFragmentType(max_length=8, null=True) # enum('data','protocol','animal')
    attachment             = models.CharField(max_length=256, null=True)
    attachment_type        = EnumFragmentAttachmentType(max_length=12, null=True) # enum('morph_figure','morph_table')
    cell_id                = models.IntegerField(null=True)
    parameter              = models.CharField(max_length=64, null=True)
    interpretation         = models.CharField(max_length=64, null=True)
    interpretation_notes   = models.TextField(null=True)
    linking_cell_id        = models.IntegerField(null=True)
    linking_pmid_isbn      = models.BigIntegerField(null=True)
    linking_pmid_isbn_page = models.IntegerField(null=True)
    linking_quote          = models.TextField(null=True)
    linking_page_location  = models.CharField(max_length=64, null=True)
    class Meta:
        db_table = 'Fragment'

class FragmentTypeRel(models.Model):
    id          = models.AutoField(primary_key=True)
    dt          = models.DateTimeField(auto_now_add=True)
    Fragment_id = models.IntegerField(db_index=True, unique=False, null=True)
    Type_id     = models.IntegerField(db_index=True, unique=False, null=True)
    priority    = models.NullBooleanField(null=True)
    class Meta:
        db_table = 'FragmentTypeRel'

class ingest_errors(models.Model):
    id                          = models.AutoField(primary_key=True)
    dt                          = models.DateTimeField(auto_now_add=True)
    field                       = models.CharField(max_length=64, null=True)
    value                       = models.CharField(max_length=64, null=True)
    filename                    = models.CharField(max_length=64, null=True)
    file_row_num                = models.IntegerField(unique=False, null=True)
    comment                     = models.CharField(max_length=255, null=True)
    class Meta:
        db_table = 'ingest_errors'
        
class Markerdata(models.Model):
    id         = models.AutoField(primary_key=True)
    dt         = models.DateTimeField(auto_now_add=True)
    expression = models.CharField(max_length=64, null=True)
    animal     = models.CharField(max_length=64, null=True)
    protocol   = models.CharField(max_length=64, null=True)
    class Meta:
        db_table = 'Markerdata'

class Property(models.Model):
    id        = models.AutoField(primary_key=True)
    dt        = models.DateTimeField(auto_now_add=True)
    subject   = models.CharField(max_length=45, null=True)
    predicate = models.CharField(max_length=45, null=True)
    object    = models.CharField(max_length=45, null=True)
    class Meta:
        db_table = 'Property'

class Synonym(models.Model):
    id      = models.AutoField(primary_key=True)
    dt      = models.DateTimeField(auto_now_add=True)
    name    = models.CharField(max_length=255, null=True)
    cell_id = models.IntegerField(null=True)
    class Meta:
        db_table = 'Synonym'

class SynonymTypeRel(models.Model):
    id          = models.AutoField(primary_key=True)
    dt          = models.DateTimeField(auto_now_add=True)
    Synonym_id  = models.IntegerField(db_index=True, unique=False, null=True)
    Type_id     = models.IntegerField(db_index=True, unique=False, null=True)
    class Meta:
        db_table = 'SynonymTypeRel'

class Term(models.Model):
    id              = models.AutoField(primary_key=True)
    dt              = models.DateTimeField(auto_now_add=True)
    parent          = models.CharField(max_length=400, null=True)
    concept         = models.CharField(max_length=400, null=True)
    term            = models.CharField(max_length=400, null=True)
    resource_rank   = models.IntegerField(null=True)
    resource        = models.CharField(max_length=200, null=True)
    portal          = models.CharField(max_length=200, null=True)
    repository      = models.CharField(max_length=200, null=True)
    unique_id       = models.CharField(max_length=400, null=True)
    definition_link = models.CharField(max_length=5000, null=True)
    definition      = models.CharField(max_length=5000, null=True)
    protein_gene    = models.CharField(max_length=100, null=True)
    human_rat       = models.CharField(max_length=100, null=True)
    control         = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = 'Term'

class Type(models.Model):
    id          = models.AutoField(primary_key=True)
    position    = models.IntegerField(null=True)
    dt          = models.DateTimeField(auto_now_add=True)
    subregion   = models.CharField(max_length=8, null=True)
    name        = models.CharField(max_length=255, null=True)
    nickname    = models.CharField(max_length=64, null=True)
    excit_inhib = EnumTypeExcitInhib(max_length=1, null=True) # enum('e','i')
    status      = EnumTypeStatus(max_length=6, null=True) # enum('active','frozen')
    notes       = models.TextField(null=True)
    class Meta:
        db_table = 'Type'

class TypeTypeRel(models.Model):
    id                  = models.AutoField(primary_key=True)
    dt                  = models.DateTimeField(auto_now_add=True)
    Type1_id            = models.IntegerField(db_index=True, unique=False, null=True)
    Type2_id            = models.IntegerField(db_index=True, unique=False, null=True)
    connection_status   = EnumTypeTypeConnectionStatus(max_length=8, null=True) # enum('positive','negative')
    connection_location = models.CharField(max_length=16, null=True)
    class Meta:
        db_table = 'TypeTypeRel'



