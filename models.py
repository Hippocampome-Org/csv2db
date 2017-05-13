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
                  ('morph_figure',  'Morph_figure'),  ('morph_table',  'Morph_table'),
                  ('fp_figure',  'Fp_figure'),  ('fp_table',  'Fp_table')]
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
        values = [('positive', 'Positive'), ('negative', 'Negative'), ('potential', 'Potential')]
        super(EnumTypeTypeConnectionStatus, self).__init__(*args, choices=values, **kwargs)

# Enum values for pattern_definition field
class EnumFiringPatternDefinitionParameter(EnumField, models.CharField):
    def __init__(self, *args, choices=[], **kwargs):
        values = [('definition', 'Definition'), ('parameter', 'Parameter'),('none', 'None')]
        super(EnumFiringPatternDefinitionParameter, self).__init__(*args, choices=values, **kwargs)

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
    pc_flag                   = models.NullBooleanField(null=True)
    soma_pcl_flag             = models.NullBooleanField(null=True)
    ax_de_pcl_flag            = models.IntegerField(unique=False,null=True)
    perisomatic_targeting_flag= models.IntegerField(unique=False,null=True)
    supplemental_pmids        = models.CharField(max_length=256, null=True)
    class Meta:
        db_table = 'EvidencePropertyTypeRel'


# table to store firing definition and parameter
class FiringPattern(models.Model):
    id                                  = models.AutoField(primary_key=True)
    overall_fp                          = models.CharField(max_length=128, null=True)
    fp_name                             = models.CharField(db_index=True, max_length=128, null=True)
    delay_ms                            = models.CharField(max_length=128, null=True)
    pfs_ms                              = models.CharField(max_length=128, null=True)
    swa_mv                              = models.CharField(max_length=128, null=True)
    nisi                                = models.CharField(max_length=128, null=True)
    isiav_ms                            = models.CharField(max_length=128, null=True)
    sd_ms                               = models.CharField(max_length=128, null=True)
    max_isi_ms                          = models.CharField(max_length=128, null=True)
    min_isi_ms                          = models.CharField(max_length=128, null=True)
    first_isi_ms                        = models.CharField(max_length=128, null=True)
    isiav1_2_ms                         = models.CharField(max_length=128, null=True)
    isiav1_3_ms                         = models.CharField(max_length=128, null=True)
    isiav1_4_ms                         = models.CharField(max_length=128, null=True)
    last_isi_ms                         = models.CharField(max_length=128, null=True)
    isiavn_n_1_ms                       = models.CharField(max_length=128, null=True)
    isiavn_n_2_ms                       = models.CharField(max_length=128, null=True)
    isiavn_n_3_ms                       = models.CharField(max_length=128, null=True)
    maxisi_minisi                       = models.CharField(max_length=128, null=True)
    maxisin_isin_m1                     = models.CharField(max_length=128, null=True)  
    maxisin_isin_p1                     = models.CharField(max_length=128, null=True) 
    ai                                  = models.CharField(max_length=128, null=True)
    rdmax                               = models.CharField(max_length=128, null=True)
    df                                  = models.CharField(max_length=128, null=True)
    sf                                  = models.CharField(max_length=128, null=True)
    tmax_scaled                         = models.CharField(max_length=128, null=True)
    isimax_scaled                       = models.CharField(max_length=128, null=True)
    isiav_scaled                        = models.CharField(max_length=128, null=True)
    sd_scaled                           = models.CharField(max_length=128, null=True)
    slope                               = models.CharField(max_length=128, null=True)
    intercept                           = models.CharField(max_length=128, null=True)
    slope1                              = models.CharField(max_length=128, null=True)
    intercept1                          = models.CharField(max_length=128, null=True)
    css_yc1                             = models.CharField(max_length=128, null=True)
    xc1                                 = models.CharField(max_length=128, null=True)
    slope2                              = models.CharField(max_length=128, null=True)
    intercept2                          = models.CharField(max_length=128, null=True)
    slope3                              = models.CharField(max_length=128, null=True)
    intercept3                          = models.CharField(max_length=128, null=True)
    xc2                                 = models.CharField(max_length=128, null=True)
    yc2                                 = models.CharField(max_length=128, null=True)   
    f1_2                                = models.CharField(max_length=128, null=True)
    f1_2crit                            = models.CharField(max_length=128, null=True)
    f2_3                                = models.CharField(max_length=128, null=True)
    f2_3crit                            = models.CharField(max_length=128, null=True)
    f3_4                                = models.CharField(max_length=128, null=True)
    f3_4crit                            = models.CharField(max_length=128, null=True)
    p1_2                                = models.CharField(max_length=128, null=True)
    p2_3                                = models.CharField(max_length=128, null=True)
    p3_4                                = models.CharField(max_length=128, null=True)
    p1_2uv                              = models.CharField(max_length=128, null=True)
    p2_3uv                              = models.CharField(max_length=128, null=True)
    p3_4uv                              = models.CharField(max_length=128, null=True)
    isii_isii_m1                        = models.CharField(max_length=128, null=True)
    i                                   = models.CharField(max_length=128, null=True)
    isiav_i_n_isi1_i_m1                 = models.CharField(max_length=128, null=True)
    maxisij_isij_m1                     = models.CharField(max_length=128, null=True)
    maxisij_isij_p1                     = models.CharField(max_length=128, null=True)
    nisi_c                              = models.CharField(max_length=128, null=True)
    isiav_ms_c                          = models.CharField(max_length=128, null=True)
    maxisi_ms_c                         = models.CharField(max_length=128, null=True)
    minisi_ms_c                         = models.CharField(max_length=128, null=True)
    first_isi_ms_c                      = models.CharField(max_length=128, null=True)
    tmax_scaled_c                       = models.CharField(max_length=128, null=True)
    isimax_scaled_c                     = models.CharField(max_length=128, null=True)
    isiav_scaled_c                      = models.CharField(max_length=128, null=True)
    sd_scaled_c                         = models.CharField(max_length=128, null=True)
    slope_c                             = models.CharField(max_length=128, null=True)
    intercept_c                         = models.CharField(max_length=128, null=True)
    slope1_c                            = models.CharField(max_length=128, null=True)
    intercept1_c                        = models.CharField(max_length=128, null=True)
    css_yc1_c                           = models.CharField(max_length=128, null=True)
    xc1_c                               = models.CharField(max_length=128, null=True)
    slope2_c                            = models.CharField(max_length=128, null=True)
    intercept2_c                        = models.CharField(max_length=128, null=True)
    slope3_c                            = models.CharField(max_length=128, null=True)
    intercept3_c                        = models.CharField(max_length=128, null=True)
    xc2_c                               = models.CharField(max_length=128, null=True)
    yc2_c                               = models.CharField(max_length=128, null=True)
    f1_2_c                              = models.CharField(max_length=128, null=True)
    f1_2crit_c                          = models.CharField(max_length=128, null=True)
    f2_3_c                              = models.CharField(max_length=128, null=True)
    f2_3crit_c                          = models.CharField(max_length=128, null=True)
    f3_4_c                              = models.CharField(max_length=128, null=True)
    f3_4crit_c                          = models.CharField(max_length=128, null=True)
    p1_2_c                              = models.CharField(max_length=128, null=True)
    p2_3_c                              = models.CharField(max_length=128, null=True)
    p3_4_c                              = models.CharField(max_length=128, null=True)
    p1_2uv_c                            = models.CharField(max_length=128, null=True)
    p2_3uv_c                            = models.CharField(max_length=128, null=True)
    p3_4uv_c                            = models.CharField(max_length=128, null=True)
    m_2p                                = models.CharField(max_length=128, null=True)
    c_2p                                = models.CharField(max_length=128, null=True)
    m_3p                                = models.CharField(max_length=128, null=True)
    c1_3p                               = models.CharField(max_length=128, null=True)
    c2_3p                               = models.CharField(max_length=128, null=True)
    m1_4p                               = models.CharField(max_length=128, null=True)
    c1_4p                               = models.CharField(max_length=128, null=True)
    m2_4p                               = models.CharField(max_length=128, null=True)
    c2_4p                               = models.CharField(max_length=128, null=True)
    n_isi_cut_3p                        = models.CharField(max_length=256, null=True)
    n_isi_cut_4p                        = models.CharField(max_length=128, null=True)
    f_12                                = models.CharField(max_length=128, null=True)
    f_crit_12                           = models.CharField(max_length=128, null=True)
    f_23                                = models.CharField(max_length=128, null=True)
    f_crit_23                           = models.CharField(max_length=128, null=True)
    f_34                                = models.CharField(max_length=128, null=True)
    f_crit_34                           = models.CharField(max_length=128, null=True)
    p_12                                = models.CharField(max_length=128, null=True)
    p_12_uv                             = models.CharField(max_length=128, null=True)
    p_23                                = models.CharField(max_length=128, null=True)
    p_23_uv                             = models.CharField(max_length=128, null=True)
    p_34                                = models.CharField(max_length=128, null=True)
    p_34_uv                             = models.CharField(max_length=128, null=True)
    m_fasp                              = models.CharField(max_length=128, null=True)
    c_fasp                              = models.CharField(max_length=128, null=True)
    n_isi_cut_fasp                      = models.CharField(max_length=128, null=True)
    definition_parameter                = EnumFiringPatternDefinitionParameter(max_length=10, null=True) # enum('definition','parameter') 
    class Meta:
        db_table = 'FiringPattern'

# firing pattern parameter mapping to evidence
class FiringPatternRel(models.Model):
    id                  = models.AutoField(primary_key=True)
    FiringPattern_id    = models.IntegerField(db_index=True, unique=False, null=True)
    Type_id             = models.IntegerField(db_index=True, unique=False, null=True)
    figure_no           = models.CharField(max_length=64, null=True)
    original_id         = models.BigIntegerField(null=True)
    istim_pa            = models.CharField(max_length=64, null=True)
    tstim_ms            = models.CharField(max_length=64, null=True)
    class Meta:
        db_table = 'FiringPatternRel'

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
    linking_page_location  = models.CharField(max_length=256, null=True)
    species_tag            = models.CharField(max_length=512, null=True)
    species_descriptor     = models.CharField(max_length=512, null=True)
    age_weight             = models.CharField(max_length=512, null=True)
    protocol               = models.CharField(max_length=512, null=True)
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

class Onhold(models.Model):
    id          = models.AutoField(primary_key=True)
    dt          = models.DateTimeField(auto_now_add=True)
    name        = models.CharField(max_length=255, null=True)
    Type_id     = models.IntegerField(db_index=True, unique=False, null=True)
    subregion   = models.CharField(max_length=8, null=True)
    pmid_isbn   = models.BigIntegerField(null=True)
    class Meta:
        db_table = 'Onhold'

class Property(models.Model):
    id        = models.AutoField(primary_key=True)
    dt        = models.DateTimeField(auto_now_add=True)
    subject   = models.CharField(max_length=45, null=True)
    predicate = models.CharField(max_length=45, null=True)
    object    = models.CharField(max_length=256, null=True)
    class Meta:
        db_table = 'Property'

class SpikeTime(models.Model):
    id                      = models.AutoField(primary_key=True)
    dt                      = models.DateTimeField(auto_now_add=True)
    FiringPattern_id        = models.IntegerField(null=True)
    spike_name              = models.CharField(max_length=128, null=True)
    spike_data              = models.CharField(max_length=128, null=True)
    class Meta:
        db_table = 'SpikeTime'

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
    supertype   = models.CharField(max_length=255, null=True)
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




